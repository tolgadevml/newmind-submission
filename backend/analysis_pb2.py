# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: analysis.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 29, 0, "", "analysis.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0e\x61nalysis.proto""\n\x0e\x41nalyzeRequest\x12\x10\n\x08\x63omments\x18\x01 \x03(\t"%\n\x07Opinion\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t"f\n\x0bTopicResult\x12\x10\n\x08topic_id\x18\x01 \x01(\t\x12\x15\n\rtopic_summary\x18\x02 \x01(\t\x12\x1a\n\x08opinions\x18\x03 \x03(\x0b\x32\x08.Opinion\x12\x12\n\nconclusion\x18\x04 \x01(\t"/\n\x0f\x41nalyzeResponse\x12\x1c\n\x06topics\x18\x01 \x03(\x0b\x32\x0c.TopicResult2?\n\x0f\x41nalysisService\x12,\n\x07\x41nalyze\x12\x0f.AnalyzeRequest\x1a\x10.AnalyzeResponseb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "analysis_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_ANALYZEREQUEST"]._serialized_start = 18
    _globals["_ANALYZEREQUEST"]._serialized_end = 52
    _globals["_OPINION"]._serialized_start = 54
    _globals["_OPINION"]._serialized_end = 91
    _globals["_TOPICRESULT"]._serialized_start = 93
    _globals["_TOPICRESULT"]._serialized_end = 195
    _globals["_ANALYZERESPONSE"]._serialized_start = 197
    _globals["_ANALYZERESPONSE"]._serialized_end = 244
    _globals["_ANALYSISSERVICE"]._serialized_start = 246
    _globals["_ANALYSISSERVICE"]._serialized_end = 309
# @@protoc_insertion_point(module_scope)
