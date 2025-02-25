#!/bin/sh

exec sply_chat_interact.py \
  model_id="$sply_model_id" \
  editor="$sply_editor" \
  user_name="$sply_user_name" \
  user_desc="$sply_user_desc" \
  ai_name="$sply_ai_name" \
  ai_desc="$sply_ai_desc" \
  in_suffix="$sply_in_suffix" \
  in_suffix_enabled="$sply_in_suffix_enabled" \
  rev_prompt="$sply_rev_prompt" \
  prompt_file="$sply_prompt_file" \
  prompt="$sply_prompt" \
  seed="$sply_seed" \
  temp="$sply_temp" \
  num_ctx="$sply_num_ctx" \
  $@

