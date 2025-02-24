#include "flexflow/ops/lora_linear.h"
#include "flexflow/ffconst_utils.h"
#include "flexflow/layer.h"
#include "flexflow/model.h"
#include "flexflow/ops/kernels/lora_linear_kernels.h"
#include "flexflow/request_manager.h"
#include "flexflow/utils/hash_utils.h"
#include "flexflow/utils/peft_weight_allocator.h"
#include "legion/legion_utilities.h"
#include <sys/stat.h>
#include <sys/types.h>
#if defined(FF_USE_CUDA) || defined(FF_USE_HIP_CUDA)
#include "flexflow/utils/cuda_helper.h"
#else
#include "flexflow/utils/hip_helper.h"
#endif

namespace FlexFlow {

// declare Legion names
using Legion::ArgumentMap;
using Legion::Context;
using Legion::coord_t;
using Legion::Domain;
using Legion::Future;
using Legion::FutureMap;
using Legion::IndexLauncher;
using Legion::InlineLauncher;
using Legion::Machine;
using Legion::Memory;
using Legion::PhysicalRegion;
using Legion::Predicate;
using Legion::Rect;
using Legion::RegionRequirement;
using Legion::Runtime;
using Legion::Task;
using Legion::TaskArgument;
using Legion::TaskLauncher;

using namespace FlexFlow::Kernels::LoraLinear;

bool check_lora_layer_match(Layer *potential_target,
                            std::string target_module_name) {
  if (potential_target->op_type == OP_LINEAR &&
      potential_target->name != nullptr && strlen(potential_target->name) > 0) {
    std::string s(potential_target->name);
    if (s.find(target_module_name) != std::string::npos &&
        s.find("lora") == std::string::npos) {
      return true;
    }
  }
  return false;
}

void FFModel::add_lora_layers(std::vector<std::string> target_modules) {
  assert(config.enable_peft &&
         "Cannot add a LoRA layer if PEFT mode is not enabled");
  assert(target_modules.size() > 0 && "LoRA target module name is empty");
  RequestManager *rm = RequestManager::get_request_manager();
  int max_lora_rank = rm->get_max_lora_rank();
  int max_concurrent_adapters = rm->get_max_concurrent_adapters();
  assert(max_lora_rank > 1 && max_lora_rank <= 32 && "Invalid max LoRA rank");
  assert(max_concurrent_adapters > 0 &&
         "Invalid number of LoRA concurrent adapters");

  for (std::string target_module_name : target_modules) {
    assert(target_module_name.length() > 0 &&
           "LoRA target module name is empty");
    // find target layer
    for (auto it = layers.begin(); it != layers.end(); ++it) {
      Layer *target_module = *it;
      bool match = check_lora_layer_match(target_module, target_module_name);
      if (!match) {
        continue;
      }
      assert(base_layer_to_peft_layer.find(target_module) ==
                 base_layer_to_peft_layer.end() &&
             "LoRA layer already added, attempting to add again");
      // Get input and output tensors from target module
      Tensor const input = target_module->inputs[0];
      Tensor const output = target_module->outputs[0];
      assert(input->data_type == output->data_type);
      // Compute OP_LORA layer name, based on target module name
      std::string name_ = target_module->name ? std::string(target_module->name)
                                              : std::string("");
      size_t last_underscore = name_.length() - 1;
      for (int i = name_.length() - 1; i > 0; i--) {
        if (!(std::isdigit(target_module->name[i]) ||
              target_module->name[i] == '_')) {
          break;
        } else if (target_module->name[i] == '_') {
          last_underscore = i;
        }
      }
      name_.erase(last_underscore);
      name_ += ".lora";
      std::cout << "Adding layer " << name_ << std::endl;
      // Create OP_LORA layer given input, output and name
      Layer *peft_layer = new Layer(this,
                                    OP_LORA,
                                    output->data_type,
                                    name_.c_str(),
                                    2 /*inputs*/,
                                    0 /*weights*/,
                                    1 /*outputs*/,
                                    input,
                                    output);
      // fix LoRA layer's transformer layer ID and model ID (to be the same as
      // target module)
      peft_layer->layer_guid.transformer_layer_id =
          target_module->layer_guid.transformer_layer_id;
      peft_layer->layer_guid.model_id = target_module->layer_guid.model_id;
      // set up output tensor for OP_LORA layer
      {
        int numdims = output->num_dims;
        int dims[MAX_TENSOR_DIM];
        for (int i = 0; i < numdims; i++) {
          dims[i] = output->dims[i];
        }
        peft_layer->outputs[0] =
            create_tensor_legion_ordering(numdims,
                                          dims,
                                          output->data_type,
                                          peft_layer,
                                          0,
                                          true /*create_grad*/);
      }
      // pass max_rank and max_concurrent_adapters to OP_LORA layer
      peft_layer->add_int_property("max_rank", max_lora_rank);
      peft_layer->add_int_property("max_concurrent_adapters",
                                   max_concurrent_adapters);
      it = layers.insert(it + 1, peft_layer);
      ++it;
      base_layer_to_peft_layer[target_module] = peft_layer;
    }
  }
}

Op *LoraLinear::create_operator_from_layer(
    FFModel &model,
    Layer const *layer,
    std::vector<ParallelTensor> const &inputs) {
  long long value;
  layer->get_int_property("max_rank", value);
  int max_rank = value;
  layer->get_int_property("max_concurrent_adapters", value);
  int max_concurrent_adapters = value;
  return new LoraLinear(model,
                        layer->layer_guid,
                        inputs[0],
                        inputs[1],
                        max_rank,
                        max_concurrent_adapters,
                        layer->name);
}

LoraLinear::LoraLinear(FFModel &model,
                       LoraLinear const &other,
                       ParallelTensor const input,
                       ParallelTensor const output)
    : LoraLinear(model,
                 other.layer_guid,
                 input,
                 output,
                 other.max_rank,
                 other.max_concurrent_adapters,
                 other.name) {}

LoraLinear::LoraLinear(FFModel &model,
                       Params const &params,
                       Input const &inputs,
                       char const *name)
    : LoraLinear(model,
                 params.layer_guid,
                 inputs.first,
                 inputs.second,
                 params.max_rank,
                 params.max_concurrent_adapters,
                 params.name) {}

LoraLinear::LoraLinear(
    FFModel &model,
    LayerID const &_layer_guid,
    ParallelTensor const _input,
    ParallelTensor const _output,
    int _max_rank,
    int _max_concurrent_adapters,
    // std::unordered_map<PEFTModelID, LoraLinearConfig> const &_peft_configs,
    char const *name)
    : Op(model,
         OP_LORA,
         _output->data_type,
         name,
         2 /*inputs*/,
         0 /*weights*/,
         false,
         1 /*outputs*/,
         _input,
         _output) {
  assert(_input->data_type == _output->data_type);
  // overwrite layer_guid
  layer_guid = _layer_guid;
  data_type = _output->data_type;

  ParallelTensorShape input_shape = this->inputs[0]->get_shape();
  LoraLinearParams params = this->get_params();

  // Create output tensor
  {
    int numdim = inputs[1]->num_dims;
    ParallelDim dims[MAX_TENSOR_DIM];
    for (int i = 0; i < numdim; i++) {
      dims[i] = inputs[1]->dims[i];
    }
    outputs[0] = model.create_parallel_tensor_legion_ordering(
        numdim, dims, inputs[1]->data_type, this);
  }
  // for (auto const &kv : _peft_configs) {
  //   peft_configs.insert(kv);
  // }
  max_rank = _max_rank;
  max_concurrent_adapters = _max_concurrent_adapters;
  // assert(check_output_input_weight_parallel_dims(allocate_weights));
}

void LoraLinear::init(FFModel const &ff) {
  assert(false && "LoraLinear does not support normal init");
}

void LoraLinear::init_inference(
    FFModel const &ff,
    std::vector<ParallelTensor> const &batch_inputs,
    std::vector<ParallelTensor> const &batch_outputs,
    MachineView const *mv) {
  assert(check_output_input_weight_same_parallel_is());
  assert(batch_inputs.size() == 2);
  assert(batch_outputs.size() == 1);
  // Assert that the output and the second input are mapped to the same
  // region/part
  assert(batch_outputs[0]->region == batch_inputs[1]->region);
  assert(batch_outputs[0]->part == batch_inputs[1]->part);
  // assert(check_output_input_weight_same_machine_view());
  // output is considered as an input to allow in-place optimization
  ParallelTensor output_tensor = batch_outputs[0];
  parallel_is = output_tensor->parallel_is;
  ArgumentMap argmap;
  Context ctx = ff.config.lg_ctx;
  Runtime *runtime = ff.config.lg_hlr;
  MachineView const *view = mv ? mv : &output_tensor->machine_view;
  size_t machine_view_hash = view->hash();
  set_argumentmap_for_init_inference(ff, argmap, output_tensor);
  IndexLauncher launcher(LORA_LINEAR_INIT_TASK_ID,
                         parallel_is,
                         TaskArgument(this, sizeof(LoraLinear)),
                         argmap,
                         Predicate::TRUE_PRED,
                         false /*must*/,
                         0 /*mapper_id*/,
                         machine_view_hash);
  launcher.add_region_requirement(RegionRequirement(batch_inputs[0]->part,
                                                    0 /*projection id*/,
                                                    READ_ONLY,
                                                    EXCLUSIVE,
                                                    batch_inputs[0]->region));
  launcher.add_field(0, FID_DATA);
  launcher.add_region_requirement(RegionRequirement(batch_inputs[1]->part,
                                                    0 /*projection id*/,
                                                    READ_WRITE,
                                                    EXCLUSIVE,
                                                    batch_inputs[1]->region));
  launcher.add_field(1, FID_DATA);
  FutureMap fm = runtime->execute_index_space(ctx, launcher);
  fm.wait_all_results();
  set_opmeta_from_futuremap_inference(ff, fm, output_tensor);
}

/*
  regions[0](O): output
  regions[1](I): kernel
  regions[2](I): bias
*/
OpMeta *LoraLinear::init_task(Task const *task,
                              std::vector<PhysicalRegion> const &regions,
                              Context ctx,
                              Runtime *runtime) {
  LoraLinear const *lora = (LoraLinear *)task->args;
  FFHandler handle = *((FFHandler const *)task->local_args);
  GenericTensorAccessorR input =
      helperGetGenericTensorAccessorRO(lora->inputs[0]->data_type,
                                       regions[0],
                                       task->regions[0],
                                       FID_DATA,
                                       ctx,
                                       runtime);
  GenericTensorAccessorW output =
      helperGetGenericTensorAccessorRW(lora->outputs[0]->data_type,
                                       regions[1],
                                       task->regions[1],
                                       FID_DATA,
                                       ctx,
                                       runtime);
  int in_dim = input.domain.hi()[0] - input.domain.lo()[0] + 1;
  int out_dim = output.domain.hi()[0] - output.domain.lo()[0] + 1;
  int batch_size = output.domain.get_volume() / out_dim;
  assert(input.domain.get_volume() == in_dim * batch_size);
  assert(output.domain.get_volume() == out_dim * batch_size);

  LoraLinearMeta *m = new LoraLinearMeta(handle, lora);
  m->trainable_inputs[0] = lora->trainable_inputs[0];
  std::strcpy(m->op_name, lora->name);
  m->layer_guid = lora->layer_guid;

  int num_shards = lora->inputs[0]->dims[0].degree;
  int shard_id = task->index_point.point_data[0];
  int num_dims = lora->inputs[0]->num_dims;
  assert(in_dim == lora->inputs[0]->dims[0].size / num_shards);
  assert(out_dim ==
         lora->inputs[1]->dims[0].size / lora->inputs[1]->dims[0].degree);

  DataType dt = m->input_type[0];
  assert(dt == m->input_type[1]);
  assert(dt == m->output_type[0]);
  assert(dt == lora->inputs[0]->data_type);
  assert(dt == lora->inputs[1]->data_type);
  assert(dt == lora->outputs[0]->data_type);

  // get layer name
  assert(lora->name != nullptr &&
         "Layer name is not set, cannot determine weights location");
  std::string lora_layername = std::string(lora->name);
  std::string searchString = "lora";
  size_t found = lora_layername.find(searchString);
  if (found == std::string::npos) {
    std::cout << "LoraLinear layer name not in the right format (does not "
                 "contain word 'lora')"
              << std::endl;
    assert(false);
  }
  std::string lora_layername_substr =
      lora_layername.substr(0, found + searchString.length());

  // allocate space for lora weights
  Memory gpu_mem = get_proc_mem(Machine::get_machine(), task->target_proc);
  m->peft_memory_manager =
      new PEFTMemoryManager(gpu_mem,
                            lora->max_rank,
                            lora->max_concurrent_adapters,
                            BatchConfig::max_sequence_length(),
                            in_dim,
                            out_dim,
                            num_shards,
                            shard_id,
                            lora_layername_substr,
                            dt);
  m->peft_memory_manager->allocate_inference_memory();
  return m;
}

void LoraLinear::forward(FFModel const &ff) {
  assert(false && "LoraLinear does not support normal init");
}

FutureMap
    LoraLinear::inference(FFModel const &ff,
                          BatchConfigFuture const &bc,
                          std::vector<ParallelTensor> const &batch_inputs,
                          std::vector<ParallelTensor> const &batch_outputs,
                          MachineView const *mv) {
  assert(check_output_input_weight_same_parallel_is());
  assert(batch_inputs.size() == 2);
  assert(batch_outputs.size() == 1);
  // Assert that the output and the second input are mapped to the same
  // region/part
  assert(batch_outputs[0]->region == batch_inputs[1]->region);
  assert(batch_outputs[0]->part == batch_inputs[1]->part);
  // assert(check_output_input_weight_same_machine_view());
  // output is considered as an input to allow in-place optimization
  ParallelTensor output_tensor = batch_outputs[0];
  parallel_is = output_tensor->parallel_is;
  ArgumentMap argmap;
  Context ctx = ff.config.lg_ctx;
  Runtime *runtime = ff.config.lg_hlr;
  MachineView const *view = mv ? mv : &output_tensor->machine_view;
  size_t machine_view_hash = view->hash();
  set_argumentmap_for_inference(ff, argmap, output_tensor);
  IndexLauncher launcher(LORA_LINEAR_INF_TASK_ID,
                         parallel_is,
                         TaskArgument(nullptr, 0),
                         argmap,
                         Predicate::TRUE_PRED,
                         false /*must*/,
                         0 /*mapper_id*/,
                         machine_view_hash);
  launcher.add_future(bc);
  launcher.add_region_requirement(RegionRequirement(batch_inputs[0]->part,
                                                    0 /*projection id*/,
                                                    READ_ONLY,
                                                    EXCLUSIVE,
                                                    batch_inputs[0]->region));
  launcher.add_field(0, FID_DATA);
  launcher.add_region_requirement(RegionRequirement(batch_inputs[1]->part,
                                                    0 /*projection id*/,
                                                    READ_WRITE,
                                                    EXCLUSIVE,
                                                    batch_inputs[1]->region));
  launcher.add_field(1, FID_DATA);
  return runtime->execute_index_space(ctx, launcher);
}

void LoraLinear::inference_task(Task const *task,
                                std::vector<PhysicalRegion> const &regions,
                                Context ctx,
                                Runtime *runtime) {
  LoraLinearMeta *m = *((LoraLinearMeta **)task->local_args);
  BatchConfig const *bc = BatchConfig::from_future(task->futures[0]);
  if (bc->num_active_tokens() == 0) {
    return;
  }
  assert(regions.size() == 2);
  assert(task->regions.size() == regions.size());
  assert(m->input_type[0] == m->output_type[0]);

  GenericTensorAccessorR input = helperGetGenericTensorAccessorRO(
      m->input_type[0], regions[0], task->regions[0], FID_DATA, ctx, runtime);
  GenericTensorAccessorW output = helperGetGenericTensorAccessorRW(
      m->input_type[1], regions[1], task->regions[1], FID_DATA, ctx, runtime);
  int in_dim = input.domain.hi()[0] - input.domain.lo()[0] + 1;
  int out_dim = output.domain.hi()[0] - output.domain.lo()[0] + 1;

  // int num_infr_tokens = bc->num_active_tokens();
  // int num_peft_tokens = bc->num_finetuning_fwd_tokens();
  inference_kernel_wrapper(m, bc, input, output);

  if (m->inference_debugging) {
    assert(task->index_point.get_dim() == 1);
    int shard_id = task->index_point.point_data[0];

    // get layer name
    std::string lora_layername = std::string(m->op_name);
    std::string searchString = "lora";
    size_t found = lora_layername.find(searchString);
    if (found == std::string::npos) {
      std::cout << "LoraLinear layer name not in the right format (does not "
                   "contain word 'lora')"
                << std::endl;
      assert(false);
    }
    std::string lora_layername_substr =
        lora_layername.substr(0, found + searchString.length());
    // print layer name
    std::cout << "INF " << lora_layername_substr << std::endl;

    // build output filepath
    fs::path dst_filepath = get_dst_folder("fwd", m->decoding_step, shard_id);
    if (m->layer_guid.model_id > 0) {
      assert(false && "Model ID > 0 not supported yet");
    }
    std::string layername = "layers." +
                            std::to_string(m->layer_guid.transformer_layer_id) +
                            "." + lora_layername_substr;
    dst_filepath /= layername;

    // save batch config, if passed
    if (bc != nullptr) {
      bc->save_to_file(dst_filepath.string() + ".batch_config");
    }

    std::string filename = dst_filepath.string() + ".input_0";
    if (input.data_type == DT_FLOAT) {
      save_tensor(
          input.get_float_ptr(), input.domain.get_volume(), filename.c_str());
    } else if (input.data_type == DT_HALF) {
      save_tensor(
          input.get_half_ptr(), input.domain.get_volume(), filename.c_str());
    } else {
      assert(false);
    }

    for (int i = 0; i < bc->max_requests_per_batch(); i++) {
      if (bc->request_completed[i] ||
          bc->requestsInfo[i].peft_model_id == PEFTModelID::NO_ID) {
        continue;
      }
      std::string peft_model_config_str =
          std::string(bc->requestsInfo[i].peft_model_config_str);
      LoraLinearConfig lora_config =
          LoraLinearConfig::deserialize_from_json_string(peft_model_config_str);
      if (!lora_applies_to_this_layer(m, lora_config)) {
        continue;
      }
      LoraLinearWeight weight = m->peft_memory_manager->get_peft(
          bc->requestsInfo[i].peft_model_id, lora_config);
      fs::path dst_filepath_weights =
          get_dst_folder("weights", m->decoding_step, shard_id) / layername;
      std::string filenameA =
          dst_filepath_weights.string() + ".weight_A.original";
      std::string filenameB =
          dst_filepath_weights.string() + ".weight_B.original";
      if (m->input_type[0] == DT_FLOAT) {
        save_tensor((float *)weight.w0_ptr,
                    lora_config.rank * in_dim,
                    filenameA.c_str());
        save_tensor((float *)weight.w1_ptr,
                    lora_config.rank * out_dim,
                    filenameB.c_str());
      } else if (m->input_type[0] == DT_HALF) {
        save_tensor((half *)weight.w0_ptr,
                    lora_config.rank * in_dim,
                    filenameA.c_str());
        save_tensor((half *)weight.w1_ptr,
                    lora_config.rank * out_dim,
                    filenameB.c_str());
      } else {
        assert(false && "Data type not supported");
      }

      if (bc->requestsInfo[i].finetuning_request) {
        int num_tokens = input.domain.get_volume() / in_dim;
        // input activation (intermediate)
        filename = dst_filepath.string() + ".low_rank_activation";
        if (output.data_type == DT_FLOAT) {
          save_tensor((float *)weight.low_rank_activation,
                      lora_config.rank * num_tokens,
                      filename.c_str());
        } else if (output.data_type == DT_HALF) {
          save_tensor((half *)weight.low_rank_activation,
                      lora_config.rank * num_tokens,
                      filename.c_str());
        } else {
          assert(false);
        }
      }
    }

    filename = dst_filepath.string() + ".output_0";
    if (output.data_type == DT_FLOAT) {
      save_tensor(
          output.get_float_ptr(), output.domain.get_volume(), filename.c_str());
    } else if (output.data_type == DT_HALF) {
      save_tensor(
          output.get_half_ptr(), output.domain.get_volume(), filename.c_str());
    } else {
      assert(false);
    }

    m->decoding_step++;
  }
}

FutureMap LoraLinear::peft_bwd(FFModel const &ff,
                               BatchConfigFuture const &bc,
                               std::vector<ParallelTensor> const &batch_inputs,
                               std::vector<ParallelTensor> const &batch_outputs,
                               MachineView const *mv) {
  assert(batch_inputs.size() == 2);
  assert(batch_outputs.size() == 1);
  // Assert that the output and the second input are mapped to the same
  // region/part
  assert(batch_outputs[0]->region == batch_inputs[1]->region);
  assert(batch_outputs[0]->part == batch_inputs[1]->part);
  ArgumentMap argmap;
  Context ctx = ff.config.lg_ctx;
  Runtime *runtime = ff.config.lg_hlr;
  ParallelTensor output_tensor = batch_outputs[0];
  parallel_is = output_tensor->parallel_is;
  MachineView const *view = mv ? mv : &output_tensor->machine_view;
  set_argumentmap_for_inference(ff, argmap, output_tensor);
  size_t machine_view_hash = view->hash();
  IndexLauncher launcher(LORA_LINEAR_PEFT_BWD_TASK_ID,
                         parallel_is,
                         TaskArgument(nullptr, 0),
                         argmap,
                         Predicate::TRUE_PRED,
                         false /*must*/,
                         0 /*mapper_id*/,
                         machine_view_hash);
  launcher.concurrent = true;
  launcher.add_future(bc);
  launcher.add_region_requirement(
      RegionRequirement(batch_inputs[0]->part_grad,
                        0 /*projection id*/,
                        reset_input_grads[0] ? WRITE_ONLY : READ_WRITE,
                        EXCLUSIVE,
                        batch_inputs[0]->region_grad));
  launcher.add_field(0, FID_DATA);
  launcher.add_region_requirement(
      RegionRequirement(batch_inputs[1]->part_grad,
                        0 /*projection id*/,
                        reset_input_grads[1] ? WRITE_ONLY : READ_WRITE,
                        EXCLUSIVE,
                        batch_inputs[1]->region_grad));
  launcher.add_field(1, FID_DATA);
  return runtime->execute_index_space(ctx, launcher);
}

void lora_inference_debugging(LoraLinearMeta *m,
                              BatchConfig const *bc,
                              GenericTensorAccessorW input_grad,
                              GenericTensorAccessorR output_grad,
                              int shard_id) {
  int in_dim = input_grad.domain.hi()[0] - input_grad.domain.lo()[0] + 1;
  int out_dim = output_grad.domain.hi()[0] - output_grad.domain.lo()[0] + 1;
  // get layer name
  std::string lora_layername = std::string(m->op_name);
  std::string searchString = "lora";
  size_t found = lora_layername.find(searchString);
  if (found == std::string::npos) {
    std::cout << "LoraLinear layer name not in the right format (does not "
                 "contain word 'lora')"
              << std::endl;
    assert(false);
  }
  std::string lora_layername_substr =
      lora_layername.substr(0, found + searchString.length());
  // print layer name
  std::cout << "BWD " << lora_layername_substr << std::endl;

  // build output filepath
  fs::path dst_filepath = get_dst_folder("bwd", m->bwd_step, shard_id);
  if (m->layer_guid.model_id > 0) {
    assert(false && "Model ID > 0 not supported yet");
  }
  std::string layername = "layers." +
                          std::to_string(m->layer_guid.transformer_layer_id) +
                          "." + lora_layername_substr;
  dst_filepath /= layername;

  assert(
      bc->peft_bwd_applies_to_this_layer(m->layer_guid.transformer_layer_id));
  int i = bc->finetuning_request_index();
  std::string peft_model_config_str =
      std::string(bc->requestsInfo[i].peft_model_config_str);
  LoraLinearConfig lora_config =
      LoraLinearConfig::deserialize_from_json_string(peft_model_config_str);
  if (!lora_applies_to_this_layer(m, lora_config)) {
    return;
  }

  // save batch config, if passed
  if (bc != nullptr) {
    bc->save_to_file(dst_filepath.string() + ".batch_config");
  }

  // weights, weights gradients
  fs::path dst_filepath_weights =
      get_dst_folder("weights", m->bwd_step, shard_id) / layername;

  LoraLinearWeight weight = m->peft_memory_manager->get_peft(
      bc->requestsInfo[i].peft_model_id, lora_config);
  std::string filename_weight_A =
      dst_filepath_weights.string() + ".weight_A.finetuned";
  std::string filename_weight_B =
      dst_filepath_weights.string() + ".weight_B.finetuned";
  std::string filename_grad_A =
      dst_filepath_weights.string() + ".weight_A.gradient";
  std::string filename_grad_B =
      dst_filepath_weights.string() + ".weight_B.gradient";
  if (m->input_type[0] == DT_FLOAT) {
    // weight A
    save_tensor((float *)weight.w0_ptr,
                lora_config.rank * in_dim,
                filename_weight_A.c_str());
    // weight grad A
    save_tensor((float *)weight.w0_grad_ptr,
                lora_config.rank * in_dim,
                filename_grad_A.c_str());
    // weight B
    save_tensor((float *)weight.w1_ptr,
                lora_config.rank * out_dim,
                filename_weight_B.c_str());
    // weight grad B
    save_tensor((float *)weight.w1_grad_ptr,
                lora_config.rank * out_dim,
                filename_grad_B.c_str());
  } else if (m->input_type[0] == DT_HALF) {
    // weight A
    save_tensor((half *)weight.w0_ptr,
                lora_config.rank * in_dim,
                filename_weight_A.c_str());
    // weight grad A
    save_tensor((half *)weight.w0_grad_ptr,
                lora_config.rank * in_dim,
                filename_grad_A.c_str());
    // weight B
    save_tensor((half *)weight.w1_ptr,
                lora_config.rank * out_dim,
                filename_weight_B.c_str());
    // weight grad B
    save_tensor((half *)weight.w1_grad_ptr,
                lora_config.rank * out_dim,
                filename_grad_B.c_str());
  } else {
    assert(false && "Data type not supported");
  }

  std::string filename = dst_filepath.string() + ".input_gradient_0";
  if (input_grad.data_type == DT_FLOAT) {
    save_tensor(input_grad.get_float_ptr(),
                input_grad.domain.get_volume(),
                filename.c_str());
  } else if (input_grad.data_type == DT_HALF) {
    save_tensor(input_grad.get_half_ptr(),
                input_grad.domain.get_volume(),
                filename.c_str());
  } else {
    assert(false);
  }

  filename = dst_filepath.string() + ".output_gradient_0";
  if (output_grad.data_type == DT_FLOAT) {
    save_tensor(output_grad.get_float_ptr(),
                output_grad.domain.get_volume(),
                filename.c_str());
  } else if (output_grad.data_type == DT_HALF) {
    save_tensor(output_grad.get_half_ptr(),
                output_grad.domain.get_volume(),
                filename.c_str());
  } else {
    assert(false);
  }
  m->bwd_step++;
}

template <typename DT>
void save_peft_to_file(DT const *weight_ptr,
                       size_t size,
                       std::string filepath) {
  std::ofstream out(filepath, std::ios::binary);
  // Check if the file was opened successfully
  if (!out || !out.is_open() || !out.good()) {
    printf("Could not open file: %s\n", filepath.c_str());
  }
  assert(out && out.is_open() && out.good() &&
         "can't write to lora weight file path");
  std::vector<DT> host_array(size);
  copy_tensor_dev_to_host(weight_ptr, host_array.data(), size);

  size_t target_data_size = sizeof(DT) * size;
  out.write((char *)host_array.data(), target_data_size);

  size_t out_written_size = out.tellp();
  if (out_written_size != target_data_size) {
    printf("save weight data error: %lu, %lu, %lu\n",
           out_written_size,
           target_data_size,
           sizeof(DT));
    assert(false);
  }
  out.close();
}

void Kernels::LoraLinear::save_peft_weights_if_needed(LoraLinearMeta *m,
                                                      BatchConfig const *bc,
                                                      int in_dim,
                                                      int out_dim,
                                                      int shard_id) {
  std::string lora_layername = std::string(m->op_name);
  std::string searchString = "lora";
  size_t found = lora_layername.find(searchString);
  if (found == std::string::npos) {
    std::cout << "LoraLinear layer name not in the right format (does not "
                 "contain word 'lora')"
              << std::endl;
    assert(false);
  }
  std::string lora_layername_substr =
      lora_layername.substr(0, found + searchString.length());

  assert(
      bc->peft_bwd_applies_to_this_layer(m->layer_guid.transformer_layer_id));
  int i = bc->finetuning_request_index();
  std::string peft_model_config_str =
      std::string(bc->requestsInfo[i].peft_model_config_str);
  LoraLinearConfig lora_config =
      LoraLinearConfig::deserialize_from_json_string(peft_model_config_str);
  if (!lora_applies_to_this_layer(m, lora_config)) {
    return;
  }
  if (bc->requestsInfo[i].optimizer_tasks.save_updated_weights) {
    std::string weight_export_folder = join_path({
        lora_config.cache_folder,
        "finetuned_models",
        lora_config.peft_model_id,
        "weights",
        "shard_" + std::to_string(shard_id),
    });
    fs::create_directories(weight_export_folder);

    int rank = lora_config.rank;
    int w0_num_elements = rank * in_dim;
    int w1_num_elements = rank * out_dim;
    std::string w0_filepath =
        join_path({weight_export_folder, lora_layername_substr + "_A.weight"});
    std::string w1_filepath =
        join_path({weight_export_folder, lora_layername_substr + "_B.weight"});
    LoraLinearWeight weight = m->peft_memory_manager->get_peft(
        bc->requestsInfo[i].peft_model_id, lora_config);
    if (m->input_type[0] == DT_FLOAT) {
      save_peft_to_file((float *)weight.w0_ptr, w0_num_elements, w0_filepath);
      if (shard_id == 0) {
        save_peft_to_file((float *)weight.w1_ptr, w1_num_elements, w1_filepath);
      }
    } else if (m->input_type[0] == DT_HALF) {
      save_peft_to_file((half *)weight.w0_ptr, w0_num_elements, w0_filepath);
      if (shard_id == 0) {
        save_peft_to_file((half *)weight.w1_ptr, w1_num_elements, w1_filepath);
      }
    } else {
      assert(false && "Data type not supported");
    }
  }
}

bool LoraLinear::peft_bwd_task(Task const *task,
                               std::vector<PhysicalRegion> const &regions,
                               Context ctx,
                               Runtime *runtime) {
  Domain input_domain = runtime->get_index_space_domain(
      ctx, task->regions[0].region.get_index_space());
  LoraLinearMeta *m = *((LoraLinearMeta **)task->local_args);
  BatchConfig const *bc = BatchConfig::from_future(task->futures[0]);
  if (!bc->peft_bwd_applies_to_this_layer(m->layer_guid.transformer_layer_id)) {
    return false;
  }
  assert(regions.size() == 2);
  assert(task->regions.size() == regions.size());
  assert(m->input_type[0] == m->output_type[0]);
  assert(task->index_point.get_dim() == 1);
  int shard_id = task->index_point.point_data[0];

  GenericTensorAccessorW input_grad = helperGetGenericTensorAccessorRW(
      m->input_type[0], regions[0], task->regions[0], FID_DATA, ctx, runtime);
  GenericTensorAccessorR output_grad = helperGetGenericTensorAccessorRO(
      m->output_type[0], regions[1], task->regions[1], FID_DATA, ctx, runtime);

  int in_dim = input_grad.domain.hi()[0] - input_grad.domain.lo()[0] + 1;
  int out_dim = output_grad.domain.hi()[0] - output_grad.domain.lo()[0] + 1;
  // int num_infr_tokens = bc->num_active_tokens();
  // int num_peft_tokens = bc->num_finetuning_bwd_tokens();
  peft_bwd_kernel_wrapper(
      ctx, runtime, m, bc, shard_id, input_grad, output_grad);

  save_peft_weights_if_needed(m, bc, in_dim, out_dim, shard_id);

  if (m->inference_debugging) {
    lora_inference_debugging(m, bc, input_grad, output_grad, shard_id);
  }
  return true;
}

void LoraLinear::backward(FFModel const &ff) {
  assert(false && "LoraLinear does not support normal backward");
}

void LoraLinear::print_layer(FFModel const &ff) {}

void LoraLinear::map_output_tensors(FFModel &ff) {
  assert(numOutputs == 1);
  assert(numInputs == 2);
  assert(outputs[0]->get_volume() == inputs[1]->get_volume());
  outputs[0]->parallel_is = inputs[1]->parallel_is;
  outputs[0]->region = inputs[1]->region;
  outputs[0]->part = inputs[1]->part;
  outputs[0]->region_grad = inputs[1]->region_grad;
  outputs[0]->part_grad = inputs[1]->part_grad;
}

bool LoraLinear::measure_operator_cost(Simulator *sim,
                                       MachineView const &mv,
                                       CostMetrics &cost_metrics) const {
  return false;
}

bool operator==(LoraLinearParams const &lhs, LoraLinearParams const &rhs) {
  if (lhs.layer_guid == rhs.layer_guid && lhs.max_rank == rhs.max_rank &&
      lhs.max_concurrent_adapters == rhs.max_concurrent_adapters &&
      strcmp(lhs.name, rhs.name) == 0) {
    return true;
  }
  return false;
}

fs::path create_unique_temp_directory() {
  std::srand(static_cast<unsigned int>(std::time(nullptr)));

  fs::path temp_dir = fs::temp_directory_path();
  fs::path unique_path;

  do {
    std::string unique_name = "flexflow_tmp_" + std::to_string(std::rand());
    unique_path = temp_dir / unique_name;
  } while (fs::exists(unique_path));

  fs::create_directory(unique_path);
  return unique_path;
}

void serialize_string(Legion::Serializer &sez,
                      std::string string_to_serialize) {
  sez.serialize(string_to_serialize.length());
  sez.serialize(string_to_serialize.c_str(), string_to_serialize.length());
}

std::string deserialize_string(Legion::Deserializer &dez) {
  size_t string_size;
  char buffer[4096] = {0};
  dez.deserialize(string_size);
  dez.deserialize(buffer, string_size);
  return std::string(buffer);
}

void LoraLinear::serialize(Legion::Serializer &sez) const {
  sez.serialize(this->layer_guid.id);
  sez.serialize(this->layer_guid.transformer_layer_id);
  sez.serialize(this->layer_guid.model_id);
  sez.serialize(this->max_rank);
  sez.serialize(this->max_concurrent_adapters);
  sez.serialize(strlen(this->name));
  sez.serialize(this->name, strlen(this->name));
}

/* static */
using PCG::Node;
Node LoraLinear::deserialize(FFModel &ff,
                             Legion::Deserializer &dez,
                             ParallelTensor inputs[],
                             int num_inputs) {
  assert(num_inputs == 2);
  size_t id, transformer_layer_id, deserialized_model_id;
  int max_rank, max_concurrent_adapters;
  // OperatorType op_type;
  // size_t num_pefts;
  size_t name_len;
  char name[MAX_OPNAME] = {0};

  LoraLinearParams params;

  dez.deserialize(id);
  dez.deserialize(transformer_layer_id);
  dez.deserialize(deserialized_model_id);
  dez.deserialize(max_rank);
  dez.deserialize(max_concurrent_adapters);
  dez.deserialize(name_len);
  dez.deserialize(name, name_len);
  LayerID layer_guid(id, transformer_layer_id, deserialized_model_id);

  params.layer_guid = layer_guid;
  // params.type = op_type;
  params.max_rank = max_rank;
  params.max_concurrent_adapters = max_concurrent_adapters;
  strcpy(params.name, name);
  return ff.get_or_create_node<LoraLinear>({inputs[0], inputs[1]}, params);
}

Op *LoraLinear::materialize(FFModel &ff,
                            ParallelTensor inputs[],
                            int num_inputs) const {
  LoraLinearParams params = get_params();
  return new LoraLinear(ff, params, {inputs[0], inputs[1]}, this->name);
}

LoraLinearParams LoraLinear::get_params() const {
  LoraLinearParams params;
  params.layer_guid = this->layer_guid;
  params.max_rank = this->max_rank;
  params.max_concurrent_adapters = this->max_concurrent_adapters;
  // params.type = this->op_type;
  if (strlen(this->name) < MAX_OPNAME) {
    strcpy(params.name, this->name);
  }
  // params.peft_configs = this->peft_configs;
  return params;
}

bool LoraLinearParams::is_valid(
    std::pair<ParallelTensorShape, ParallelTensorShape> const &input_shape)
    const {
  return true;
}

}; // namespace FlexFlow

namespace std {
size_t hash<FlexFlow::LoraLinearParams>::operator()(
    FlexFlow::LoraLinearParams const &params) const {
  size_t key = 0;
  hash_combine(key, params.layer_guid.id);
  hash_combine(key, params.layer_guid.transformer_layer_id);
  hash_combine(key, params.layer_guid.model_id);
  hash_combine(key, params.max_rank);
  hash_combine(key, params.max_concurrent_adapters);
  return key;
}
}; // namespace std
