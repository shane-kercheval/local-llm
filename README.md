# local-llm

Create a docker container and run `ggml-vicuna-13b`

- I followed this video https://www.youtube.com/watch?v=-BidzsQYZM4 and created a corresponding dockerfile.
- build/run dockerfile via `make docker_run`




- https://www.reddit.com/r/SteamDeck/comments/12k1d8h/manual_how_to_install_large_language_model_vicuna/

https://vicuna.lmsys.org


curl -X POST -H "Authorization: Bearer token123" -H "Content-Type: application/json" -d '{"prompt": "Q: What is the capital of France? A: "}' http://localhost:8080/completions
