import replicate


def musicgen(prompt_inspiration:str) -> str:
    output = replicate.run(
        "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
        input={
            "top_k": 250,
            "top_p": 0,
            "prompt": prompt_inspiration,
            "duration": 60,
            "temperature": 1,
            "continuation": False,
            "model_version": "stereo-melody-large",
            "output_format": "mp3",
            "continuation_start": 0,
            "multi_band_diffusion": False,
            "normalization_strategy": "peak",
            "classifier_free_guidance": 3
        }
    )
    return output
