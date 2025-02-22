# TODO

## Niji Version Handling Issue
```
Ice cream icon --niji {5, 6} --style {cute, expressive} --weird {250, 1000} --ar {1:1, 2:3}
```
The error shows:
```json
"Value error, Invalid version value. Must be one of: {'6', '5', '4', '3', '2', '1', '5.2', '5.0', '5.1', '6.1'} [type=value_error, input_value='vniji 5', input_type=str]"
```

The 'v' prefix is being incorrectly added to 'niji' versions. Should be handling niji versions separately from regular versions. Here's anther example

```
python -m midjargon perm "Ice cream icon --niji {5, 6} --style {cute, expressive} --weird {250, 1000} --ar {1:1, 2:3}" -j
[
  "Ice cream icon --niji 5 --style cute --weird 250 --ar 1:1",
  "Ice cream icon --niji 5 --style cute --weird 250 --ar 2:3",
  "Ice cream icon --niji 5 --style cute --weird 1000 --ar 1:1",
  "Ice cream icon --niji 5 --style cute --weird 1000 --ar 2:3",
  "Ice cream icon --niji 5 --style expressive --weird 250 --ar 1:1",
  "Ice cream icon --niji 5 --style expressive --weird 250 --ar 2:3",
  "Ice cream icon --niji 5 --style expressive --weird 1000 --ar 1:1",
  "Ice cream icon --niji 5 --style expressive --weird 1000 --ar 2:3",
  "Ice cream icon --niji 6 --style cute --weird 250 --ar 1:1",
  "Ice cream icon --niji 6 --style cute --weird 250 --ar 2:3",
  "Ice cream icon --niji 6 --style cute --weird 1000 --ar 1:1",
  "Ice cream icon --niji 6 --style cute --weird 1000 --ar 2:3",
  "Ice cream icon --niji 6 --style expressive --weird 250 --ar 1:1",
  "Ice cream icon --niji 6 --style expressive --weird 250 --ar 2:3",
  "Ice cream icon --niji 6 --style expressive --weird 1000 --ar 1:1",
  "Ice cream icon --niji 6 --style expressive --weird 1000 --ar 2:3"
]
python -m midjargon mj "Ice cream icon --niji {5, 6} --style {cute, expressive} --weird {250, 1000} --ar {1:1, 2:3}" -j
{
  "error": "1 validation error for MidjourneyPrompt\nversion\n  Value error, Invalid version value. Must be one of: {'1', '2', '3', '4', '5', '6', '6.1', '5.1', '5.0', '5.2'} [type=value_error, input_value='vniji 5', input_type=str]\n    For further information visit https://errors.pydantic.dev/2.10/v/value_error"
}
```