# **Midjourney Prompt Format Specification**

_2025-02-06 by Adam Twardoch, not affiliated with Midjourney_

Midjourney prompts use “midjargon”, a structured syntax to instruct the Midjourney models to generate images. A prompt consists of three main sections, in order:

1. **Image Reference (Optional)**
2. **Text Description (Required if no image is provided)**
3. **Parameters (Optional)**

Each section has defined syntax and placement requirements. Advanced features such as multi-prompts with weights, permutation prompts, personalization, and style or character references are integrated into the text description and parameters.

Midjourney supports two distinct types of stylizations. The official Midjourney documentation often ambiguously calls both “style”: 

- Style reference
- Personalization

## Parameters

Parameters are modifiers appended at the end of the prompt that adjust various aspects of image generation. Parameters always begin with two hyphens `--` and may accept a value. The order of parameters (after the text description) is flexible.

Terms that follow a parameter `--a` are treated as its arguments (values). If `--a` is directly followed by another parameter `--b`, then `--a` is considered a boolean flag. 

---

## Choosing the model

### Midjourney series (`--v` or `--version`)

Uses the specified version of the general Midjourney model series. 

#### Syntax

```
--v <version_number>
```

#### Values

- `5`, `5.1`, `5.2`, `6`, `6.1`

> Example

```
--v 6
```

### Niji series (`--niji`)

Uses the specified version of the Niji model series, optimized for anime and illustrative styles.

#### Syntax

```
--niji <version_number>
```

- Values: `5`, `6`

> Example

```
--niji 6
```

### Model mode (`--style`)

Applies specific model mode. 

```
--style <mode_name>
```

- Mode name can be `raw`, it reduces automatic personalization.

> Example

```
--style raw
```

## Using images

### Image references

One or more direct image URLs or attachments used to influence the generated image's style, color, composition, and content.

Must appear at the very **start** of the prompt.

Each image can be:

- A direct image URL ending with `.png`, `.jpg`, `.jpeg`, `.gif`, or `.webp`.
- An attached image in Discord or uploaded via the Midjourney web interface.

Multiple images are separated by whitespace.

> Example

```
https://example.com/image1.jpg https://example.com/image2.png
```

#### Image weight (`--iw`)

`--iw <value>`

Adjusts the influence of all image references relative to the text prompt. 

- Value Range `0.0` to `3.0` (float)
- Default: `1.0` (varies by model)

> Example

```
--iw 1.5
```

As with other parameters, `--iw` must be placed after the text description, even though it refers to the image references that are placed at the very start of the prompt.

### Character reference (`--cref`)

`--cref <url1> [<url2> ...]`

Uses images as character references to maintain consistency.

#### Character weight (`--cw`)

Adjusts the strength of the character reference.

`--cw <value>`

- Value range: `0` to `100` (integer)
- Default: `100`

The character weight `0` typically only copies the face. 

> Example

```
--cref https://example.com/character.jpg --cw 50
```

### Style reference (`--sref`)

The `--sref` parameter uses images as style references without influencing content. It applies the visual characteristics of a specific images or stylization code. 

In effect, it pulls the generated image towards a specific look that is expressed explicitly (via the image) or less directly (via the stylization code).

```
--sref <url|code> [<url|code> ...]
```

One or more image URLs or a specific stylization CODE (the CODE acts as a shorthand for a predefined image reference)

#### Style weight (`--sw`)

Adjusts the strength of the style reference.

`--sw <value>`

- Value Range: `0` to `1000` (integer)

#### Style version (`--sv`)

Selects different style reference algorithms.

`--sv <value>`

- Values: `1`, `2`, `3`, `4`

> Example

```
--sref https://example.com/style.jpg --sw 200 --sv 2
```

#### Random style reference

`--sref random`

Generates a random style reference.

### Persona reference (`--p`)

References one or more “personas”, personalized style profiles, which pull the generated image towards the preferences or a general style of a particular user or moodboard, with the degree controlled by `--s`.

- Without specifying a persona code, `--p` uses your current personalization profile.
- Providing one or more persona codes of a personalization profile or moodboard (e.g., `--p p123456789`) applies a specific personalization.

#### Personalization weight (`--s`)

```
--stylize <value>
```

The `--s` (`--stylize`, or personalization weight) parameter controls the degree of personalization. 

- If a persona with a code is provided, the `--s` parameter controls how much the generated image will be pulled towards that persona.
- If the personalization switch is used (`--p`) without a code, the `--s` parameter controls how much the generated image will be pulled towards your current personalization profile.
- If the personalization switch is not used (no `--p` at all), the `--s` parameter controls how much the generated image will be pulled towards the model’s general “persona” (overall aesthetic preference).

- Value range: `0` to `1000` (integer)
- Default: `100`

The value of `0` applies minimal personalization, though certain influence of the model remains. To reduce the model influence, and have purer personalization use `--style raw` together with a low `--s` value.

> Example:

```
--p p123456789 --s 500 --style raw
```

## Describing the image

A natural language description of the desired image, specifying the subject, mood, style, and other artistic details.

### Clarity & specificity

Use specific adjectives, nouns, and phrases. Describe the subject, medium, environment, lighting, color, mood, and composition.

### Positive framing

Emphasize what should appear in the image rather than what should be excluded (exclusions are handled by the `--no` parameter).

### Tokenization

The text is internally tokenized; word order and precision are important.

### Text generation

Use double quotation marks `"` around words or phrases to specify exact text you want to appear in the image.

> Example

```
A neon sign that says "Open"
```

### Negative text description (`--no`)

Signals to the model elements or aspects that you don’t want to see in the image. 

```
--no <item1, item2, ...>
```

- Value: Comma-separated list of terms

> Example:

```
--no cars, trees, watermarks
```

## Image layout

### Aspect ratio (`--ar`)

Sets the width-to-height ratio of the image

```
--ar <width>:<height>
```

- Value: Two integers separated by a colon
- Default: `1:1`

> Example:

```
--ar 16:9
```

### Tile (`--tile`)

Creates images that are seamlessly tileable

```
--tile
```

- Value: None (boolean flag)

> Example:

```
--tile
```

---

## Separating and prioritizing

Use a double colon `::` to separate concepts, optionally followed by a weight. If omitted, the weight defaults to 1.

```
concept1 ::<weight1> concept2 ::<weight2> ...
```

- Weight values can be floating-point numbers within the range `-10.0` to `10.0`.
- Negative weights (e.g., `::-0.5`) de-emphasize or exclude a concept.

### Purpose

This syntax allows you to balance and blend different concepts in one prompt. Weights are normalized internally to maintain their proportional relationships.

### Examples

```
futuristic city ::2 cyberpunk skyline ::1
beautiful landscape ::1.5 mountains ::-0.5 water
serene lake ::2 foggy mountains ::1
portrait ::1.5 dramatic lighting ::1 dark background ::0.8
still life painting ::1 fruit ::-0.5
```

---

## Variation

### Chaos (`--chaos` or `--c`)

Controls variation or unpredictability in the output

```
--chaos <value>
```

- Value range: `0` to `100` (integer)
- Default: `0`

> Example

```
--chaos 50
```

### Weird (`--weird` or `--w`)

Introduces unconventional aesthetics

```
--weird <value>
```

- Value range: `0` to `3000` (integer)
- Default: `0`

> Example

```
--weird 1000
```

---

## Generation process

### Seed (`--seed`)

Sets a specific seed to reproduce outcomes

```
--seed <value>
```

- Value range: `0` to `4294967295` (integer)

> Example:

```
--seed 123456789
```

### Prompt permutation

Prompt permutation allows you to quickly generate multiple prompts by including comma-separated options within curly braces `{}`. The surrounding fixed text is repeated with each provided option to create separate prompt variations.

Enclose a comma-separated list of options within curly braces. 

```
A {red, blue, green} car
```

This expands to 3 prompts:

- `A red car`
- `A blue car`
- `A green car`

Repeat permutations.

```
A {red, blue} {car, truck} with {chrome, matte} finish
```

This expands to 2×2×2=8 prompts. 

Permute parameters.

```
portrait --ar {1:1, 16:9} --s {100, 500, 1000}
```

This expands to 2×3=6 prompts. 

Nest permutations.

```
{realistic, artistic} scene --v {5.2, 6 {, --style raw}} 
```

This expands to 2×(2+1)=6 prompts:

- `realistic scene --v 5.2`
- `realistic scene --v 6`
- `realistic scene --v 6 --style raw`
- `artistic scene --v 5.2`
- `artistic scene --v 6`
- `artistic scene --v 6 --style raw`

Within a permutation group, use commas to separate portions, prefix a comma with a backslash to actually have it in the expanded prompt.

```
A {bright\, vibrant, dark\, moody} atmosphere
```

This expands to 2 prompts:

- `A bright, vibrant atmosphere`
- `A dark, moody atmosphere`

The total number of permutations may be limited based on subscription tier. Permutation prompts are only available in Fast Mode.

Permutation is great for exploring various syntaxes and prompt structures: 

```
beautiful woman{::, ::2, ::0.3, \,} sports car
```

expands into

- `beautiful woman:: sports car`
- `beautiful woman::2 sports car`
- `beautiful woman::0.3 sports car`
- `beautiful woman, sports car`



### Repeat (`--repeat` or `--r`)

The `--r` parameter produces multiple prompts, similarly to prompt permutation, but the multiplication happens on the model side. It can be combined with permutation prompts.

If a prompt includes the `--r` parameter, the model runs the same prompt multiple times to generate variations. It can be used with `--sref random` to generate different style references each time. 

```
--repeat <number>
```

- Value range: Basic Subscribers: 2–4, Standard Subscribers: 2–10, Pro/Mega Subscribers: 2–40

> Example:

```
--repeat 5
```

## Quality and speed

### Quality (`--quality` or `--q`)

Controls the time spent generating an image; affects detail

```
--quality <value>
```

- Values: `0.25`, `0.5`, `1` (default)

> Example

```
--quality 0.5
```

#### Turbo Mode (`--turbo`)

Generates images faster using additional GPU resources

```
--turbo
```

- Value: None (boolean flag)

#### Relax Mode (`--relax`)

Generates images in relaxed mode without consuming GPU time

```
--relax
```

- Value: None (boolean flag)

### Stop (`--stop`)

Stops image generation at a specified percentage of completion for different artistic effects

```
--stop <value>
```

- Value range: `10` to `100` (integer)
- Default: `100`

> Example:

```
--stop 80
```

---

## Summary

- **Order matters**: Image prompts come first (if used), followed by the text description, and then all parameters.
- **Parameter prefix**: Every parameter starts with `--` and, if required, is followed by a space and its value.
- **Advanced techniques**: Use multi-prompts with `::` and permutation prompts with `{}` to fine-tune creative direction and generate multiple variations.
- **Personalization and references**: `--sw` controls the weight of the style reference (`--sref`). `--s` controls the weight of personalization (`--p`, or of the default persona when `--p` is not provided). Style reference and personalization operate independently: each pulls the image in a distinct stylistic direction. To test the full effect of style reference without personalization influence, use: `--style raw --s 0`.
- **Model and feature dependencies**: Some parameters (e.g., `--iw`, `--sv`, `--p`, permutation prompts) are model-specific or depend on the subscription tier or mode (e.g., Fast Mode).
- **Text generation**: Use double quotation marks `"` to specify exact text to appear in the image.

## Prompt examples

1. **Basic Text-Only Prompt:**

```
/imagine prompt: A serene sunset over the ocean
```

2. **Prompt with Image URLs, Text, and Parameters:**

```
/imagine prompt: https://example.com/inspiration.jpg A portrait of a wise old man --style raw --v 5.1
```

3. **Prompt with Character and Style References:**

```
/imagine prompt: A hero in battle --cref https://example.com/hero.png --cw 75 --sref https://example.com/style.jpg --sw 150
```

4. **Multi-Prompt with Weighting:**

```
/imagine prompt: futuristic city ::2 cyberpunk skyline ::1 --chaos 20
```

5. **Permutation Prompt for Multiple Variations:**

```
/imagine prompt: A {red, blue, green} bird on a {flower, leaf} --ar {16:9, 1:1}
```

6. **Prompt with Personalization and Parameters:**

```
/imagine prompt: A vibrant garden in spring --p p123456789 --stylize 500 --seed 987654321
```

7. **Complex Mixed Prompt:**

```
/imagine prompt: {realistic, artistic} portrait of a {young, old} {man, woman} --style {raw, expressive} --v 6 --ar 1:1 --stylize {100, 1000}
```

8. **Prompt with Exclusions and Turbo Mode:**

```
/imagine prompt: A futuristic landscape at dusk --ar 21:9 --stylize 300 --chaos 50 --seed 987654321 --no buildings, cars --turbo
```

---

## Notes for parser implementers

### Parsing order

1. **Permutation:**

- Process all permutation groups `{...}`.
- Handle nested permutations.
- Expand into individual prompts.
- `a{b, c}d` should expand to `abd` `acd`. The spaces right around the `{` and `}` should be treated as they are. Spaces around the separating commas can be collapsed fully, as if there is no space.
- `\{` `\}` `\,` must produce the literal `{` `}` `,` in the expanded permutations

2. **Image referece:**

- Identify and validate image URLs or attachments at the start.
- Check for supported file formats.
- Handle multiple images.

3. **Text description:**

- Extract main prompt text.
- Segment text by weight markers `::`.
- Handle escaped characters.
- Identify text in double quotes `"` for explicit text generation.

4. **Parameter Processing:**

- Extract parameters starting with `--`.
- Parse parameter values.
- Handle boolean flags.
- Validate parameter ranges.
- Values should be typically strings, unless it’s obviously an int or float. Version "number" should be kept a string.

### Boolean Parameters

- If a parameter is followed by another parameter (e.g., `--tile --ar 16:9`), it's treated as a boolean flag.

### Multi-Value Parameters

- Some parameters accept multiple values (e.g., `--no cars, trees`).

### Parameter Validation

- Numeric ranges are enforced.
- Aspect ratios must be valid integers.
- Version numbers must be supported.
- Style names and codes must be recognized.

### Error handling

The parser should handle common errors gracefully:

- Invalid URL formats.
- Malformed permutation syntax.
- Invalid parameter values.
- Missing required components.
- Unsupported parameter combinations.
