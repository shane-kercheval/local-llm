# local-llm

The goal of this project is to run an LLM locally and expose via API and streamlit app. The API and streamlit app can be ran via docker-compose services.

- This video was helpful in getting started with `llama_cpp` and the `vicuna` model: https://www.youtube.com/watch?v=-BidzsQYZM4

---

# Running the project

- create/start the docker services via command-line `make docker_run`
    - This may take some time, the following models are downloaded into the `/code/models` directory of the container:
        - `ggml-vicuna-13b-1.1-q4_0`
        - `ggml-alpaca-7b-q4.bin`
- (optional) you can run unit tests (note: these take around 15 seconds to run because I load both models which is slow) either with the `make tests` command by either:
    - attaching VS code to one of the containers and running the command inside the VS Code terminal
    - attaching the command line directly to the container via the command `make zsh`
- once services are started, in a separate terminal
    - run `make streamlit` to open up the streamlit app in your default browser
    - run `make api_docs` to open of the docs for the FastAPI app

To test out the API via command-line, run:

```
curl -X POST -H "Authorization: Bearer token123" -H "Content-Type: application/json" -d '{"prompt": "Q: What is the capital of France? A: "}' http://localhost:8080/completions
```

---

# Resources

- https://vicuna.lmsys.org
