# gradio iFrame

This is a custom gradio component used to display the shap package text plot. Which is interactive HTML and needs a custom wrapper.
See custom component examples at official [docu](https://www.gradio.app/guides/custom-components-in-five-minutes)

# Credit
CREDIT: based mostly of Gradio template component, HTML
see: https://www.gradio.app/docs/html

## Changes
**Addition/changes are marked. Everything else can be considered the work of other (the Gradio Team)**

#### Changes Files/Contributions
- backend/iframe.py - updating component to accept custom height/width and added new example
- demo/app.py - slightly changed demo file for better dev experience
- frontend/index.svelte - slightly changed to accept custom height/width
- frontend/HTML.svelte - updated to use iFrame and added custom function to programmatically set height values
