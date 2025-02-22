# Notes

## Using "sply_chat_interact.py"
  * Run "./sply_chat_interact.py --help" for command line options and defaults
  * Enter "/?" for help
  * Suffix input lines with a backslash to extend the input to multiple lines
  * Hit Ctrl-C during generation to interrupt and return to input mode

## Tested working models
  * [qwen2.5-coder-14b-instruct-q8_0.gguf](https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct-GGUF/blob/main/qwen2.5-coder-14b-instruct-q8_0.gguf) - Base-line for testing
  * [Qwen2.5-Coder-7B-Instruct-abliterated-Q8_0.gguf](https://huggingface.co/bartowski/Qwen2.5-Coder-7B-Instruct-abliterated-GGUF/blob/main/Qwen2.5-Coder-7B-Instruct-abliterated-Q8_0.gguf) - lacks creativity compared to the 14b version
  * [Lamarck-14B-v0.7-Q8_0.gguf](https://huggingface.co/bartowski/Lamarck-14B-v0.7-GGUF/blob/main/Lamarck-14B-v0.7-Q8_0.gguf) - Seems very creative. Not yet _heavily_ tested
  * [DeepSeek-R1-Distill-Llama-70B-abliterated-IQ3_XXS.gguf](https://huggingface.co/bartowski/huihui-ai_DeepSeek-R1-Distill-Llama-70B-abliterated-GGUF/blob/main/huihui-ai_DeepSeek-R1-Distill-Llama-70B-abliterated-IQ3_XXS.gguf) - Only tested once (because it took 23 minutes using CPU + 32 GB RAM + 16 GB swap) - but it did work, so that counts

## Mostly-working models
  * [phi-4-abliterated.Q8_0.gguf](https://huggingface.co/mradermacher/phi-4-abliterated-GGUF/blob/main/phi-4-abliterated.Q8_0.gguf) - Occasionally generates high-strangeness like multiple string results ('this''that') or markdown block-quotes. Otherwise very verbose, creative, and life-like.

## Non-working models
  * [Mistral-Small-24B-Instruct-2501-Q5_K_M.gguf](https://huggingface.co/bartowski/Mistral-Small-24B-Instruct-2501-GGUF/blob/main/Mistral-Small-24B-Instruct-2501-Q5_K_M.gguf) - generates a lot of simulated python errors.

## Dealing with gibberish output (in order of importance)
  * Try a different model - see the [tested working models list](#tested-working-models). Note that "chain of thought reasoning" models aren't well suited as they generate a lot of extraneous output 
  * Modify the prompt to show examples of expected behavior
  * Try a lower temperature value
  * Try an alternate seed number
  * Reuse a model/prompt/seed combo that has worked in the past
  * When all else fails, Ctrl-C + "edit_prompt()" are your friends

## Misc
  * The default prompt editor is "vim" - customize with the "editor=" options and parameters
  * "prompt_file=" args always have precedence over "prompt=" args
  * "edit_prompt" currently leaves prompt tempfiles intact (for manual review)
  * "make_prompt" is jailbroken - modify to taste, or provide a custom prompt

