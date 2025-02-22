# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: plugin/tensorboard_plugin_profile/protobuf/input_pipeline.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from tensorboard_plugin_profile.protobuf import diagnostics_pb2 as plugin_dot_tensorboard__plugin__profile_dot_protobuf_dot_diagnostics__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n?plugin/tensorboard_plugin_profile/protobuf/input_pipeline.proto\x12\x13tensorflow.profiler\x1a\x19google/protobuf/any.proto\x1a<plugin/tensorboard_plugin_profile/protobuf/diagnostics.proto\"\x80\x03\n\x12\x42ottleneckAnalysis\x12\x15\n\rinput_percent\x18\x07 \x01(\x01\x12\x16\n\x0eoutput_percent\x18\x08 \x01(\x01\x12\x14\n\x0cidle_percent\x18\t \x01(\x01\x12\x17\n\x0f\x63ompute_percent\x18\n \x01(\x01\x12\x1c\n\x14input_classification\x18\x01 \x01(\t\x12\x17\n\x0finput_statement\x18\x02 \x01(\t\x12$\n\x1ckernel_launch_classification\x18\x03 \x01(\t\x12\x1f\n\x17kernel_launch_statement\x18\x04 \x01(\t\x12 \n\x18\x61ll_other_classification\x18\x05 \x01(\t\x12\x1b\n\x13\x61ll_other_statement\x18\x06 \x01(\t\x12)\n!device_collectives_classification\x18\x0b \x01(\t\x12$\n\x1c\x64\x65vice_collectives_statement\x18\x0c \x01(\t\"\\\n\x0bStepSummary\x12\x0f\n\x07\x61verage\x18\x01 \x01(\x01\x12\x1a\n\x12standard_deviation\x18\x02 \x01(\x01\x12\x0f\n\x07minimum\x18\x03 \x01(\x01\x12\x0f\n\x07maximum\x18\x04 \x01(\x01\"\xe0\x02\n\x15PerGenericStepDetails\x12\x13\n\x0bstep_number\x18\x01 \x01(\x05\x12\x11\n\tstep_name\x18\x0e \x01(\t\x12\x14\n\x0cstep_time_ms\x18\x02 \x01(\x01\x12\x17\n\x0funknown_time_ms\x18\x03 \x01(\x01\x12\x1a\n\x12host_wait_input_ms\x18\x0b \x01(\x01\x12\x19\n\x11host_to_device_ms\x18\x0c \x01(\x01\x12\x11\n\toutput_ms\x18\x05 \x01(\x01\x12\x19\n\x11\x64\x65vice_compute_ms\x18\x06 \x01(\x01\x12\x1b\n\x13\x64\x65vice_to_device_ms\x18\x07 \x01(\x01\x12\x1d\n\x15\x64\x65vice_collectives_ms\x18\r \x01(\x01\x12\x17\n\x0fhost_compute_ms\x18\x08 \x01(\x01\x12\x17\n\x0fhost_prepare_ms\x18\t \x01(\x01\x12\x17\n\x0fhost_compile_ms\x18\n \x01(\x01J\x04\x08\x04\x10\x05\"\xa5\x01\n\x12InputTimeBreakdown\x12\x1d\n\x15\x64\x65manded_file_read_us\x18\x01 \x01(\x01\x12\x1d\n\x15\x61\x64vanced_file_read_us\x18\x02 \x01(\x01\x12\x18\n\x10preprocessing_us\x18\x03 \x01(\x01\x12\x12\n\nenqueue_us\x18\x04 \x01(\x01\x12#\n\x1bunclassified_non_enqueue_us\x18\x05 \x01(\x01\"\xa6\x01\n\x0eInputOpDetails\x12\x0f\n\x07op_name\x18\x01 \x01(\t\x12\r\n\x05\x63ount\x18\x02 \x01(\x04\x12\x12\n\ntime_in_ms\x18\x03 \x01(\x01\x12\x17\n\x0ftime_in_percent\x18\x04 \x01(\x01\x12\x17\n\x0fself_time_in_ms\x18\x05 \x01(\x01\x12\x1c\n\x14self_time_in_percent\x18\x06 \x01(\x01\x12\x10\n\x08\x63\x61tegory\x18\x07 \x01(\t\"\x84\x01\n#InputPipelineAnalysisRecommendation\x12\x0f\n\x07\x64\x65tails\x18\x01 \x03(\t\x12\x31\n\x13\x62ottleneck_analysis\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x19\n\x11summary_next_step\x18\x03 \x01(\t\"\x85\x06\n\x18GenericStepTimeBreakdown\x12\x41\n\x17unknown_time_ms_summary\x18\x01 \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12\x44\n\x1ahost_wait_input_ms_summary\x18\t \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12\x43\n\x19host_to_device_ms_summary\x18\n \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12:\n\x10input_ms_summary\x18\x0b \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12;\n\x11output_ms_summary\x18\x03 \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12\x43\n\x19\x64\x65vice_compute_ms_summary\x18\x04 \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12\x45\n\x1b\x64\x65vice_to_device_ms_summary\x18\x05 \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12G\n\x1d\x64\x65vice_collectives_ms_summary\x18\x0c \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12\x41\n\x17host_compute_ms_summary\x18\x06 \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12\x41\n\x17host_prepare_ms_summary\x18\x07 \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12\x41\n\x17host_compile_ms_summary\x18\x08 \x01(\x0b\x32 .tensorflow.profiler.StepSummaryJ\x04\x08\x02\x10\x03\"\x97\x05\n\x1bInputPipelineAnalysisResult\x12\x0b\n\x03tag\x18\x10 \x01(\x08\x12\x15\n\rhardware_type\x18\t \x01(\t\x12;\n\x11step_time_summary\x18\x02 \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12?\n\x15input_percent_summary\x18\x03 \x01(\x0b\x32 .tensorflow.profiler.StepSummary\x12\x15\n\rinput_percent\x18\x0b \x01(\x01\x12\x16\n\x0eoutput_percent\x18\r \x01(\x01\x12\x14\n\x0cidle_percent\x18\x0e \x01(\x01\x12\x17\n\x0f\x63ompute_percent\x18\x0f \x01(\x01\x12*\n\x0cstep_details\x18\x04 \x03(\x0b\x32\x14.google.protobuf.Any\x12\x45\n\x14input_time_breakdown\x18\x05 \x01(\x0b\x32\'.tensorflow.profiler.InputTimeBreakdown\x12=\n\x10input_op_details\x18\x06 \x03(\x0b\x32#.tensorflow.profiler.InputOpDetails\x12P\n\x0erecommendation\x18\x07 \x01(\x0b\x32\x38.tensorflow.profiler.InputPipelineAnalysisRecommendation\x12\x31\n\x13step_time_breakdown\x18\x08 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x35\n\x0b\x64iagnostics\x18\x0c \x01(\x0b\x32 .tensorflow.profiler.DiagnosticsJ\x04\x08\x01\x10\x02J\x04\x08\n\x10\x0b\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'plugin.tensorboard_plugin_profile.protobuf.input_pipeline_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _BOTTLENECKANALYSIS._serialized_start=178
  _BOTTLENECKANALYSIS._serialized_end=562
  _STEPSUMMARY._serialized_start=564
  _STEPSUMMARY._serialized_end=656
  _PERGENERICSTEPDETAILS._serialized_start=659
  _PERGENERICSTEPDETAILS._serialized_end=1011
  _INPUTTIMEBREAKDOWN._serialized_start=1014
  _INPUTTIMEBREAKDOWN._serialized_end=1179
  _INPUTOPDETAILS._serialized_start=1182
  _INPUTOPDETAILS._serialized_end=1348
  _INPUTPIPELINEANALYSISRECOMMENDATION._serialized_start=1351
  _INPUTPIPELINEANALYSISRECOMMENDATION._serialized_end=1483
  _GENERICSTEPTIMEBREAKDOWN._serialized_start=1486
  _GENERICSTEPTIMEBREAKDOWN._serialized_end=2259
  _INPUTPIPELINEANALYSISRESULT._serialized_start=2262
  _INPUTPIPELINEANALYSISRESULT._serialized_end=2925
# @@protoc_insertion_point(module_scope)
