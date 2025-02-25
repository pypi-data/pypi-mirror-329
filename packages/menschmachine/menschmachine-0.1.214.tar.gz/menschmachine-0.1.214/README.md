# MenschMachine library

## Problems / Bugs

Usage matrix:

| 	                   | OpenAI 	     | Anthropic	                 | DeepSeek	     | Gemini	                     | 	  | 	  |
|---------------------|--------------|----------------------------|---------------|-----------------------------|----|----|
| Direct      	       | 	Y with func | 	  Y with func             | 	    ?        | 	   ?                       | 	  | 	  |
| OpenRouter	         | 	  ?         | 	   Y with func            | 	   Y no func | 	   N (errors with funcs)   | 	  | 	  |
| 	     LiteLLM proxy | 	     ?      | 	    N (errors with funcs) | 	  ?          | 	     N (errors with funcs) | 	  | 	  |
| 	                   | 	            | 	                          | 	             | 	                           | 	  | 	  |

## LiteLLM

- errors when using tools with anthropic and gemini (different errors)

### OpenRouter

- gemini hangs after first tool result

## TODO

- retry failed patch as aider does
- MM().ask(prompt, max_costs=0.10)
- add whoosh for local (file) search
- Change Remove Operation from first line (contents) to last line (content) 
- add a line-numbering agent for callbacks for Remove-Operatin 