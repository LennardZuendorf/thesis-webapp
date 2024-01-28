# HTML component that implements custom iFrame

<script lang="ts">
	import { createEventDispatcher } from "svelte";
	export let elem_classes: string[] = [];
	export let value: string;
	export let visible = true;
	export let min_height = false;

	# default setting height and width
	export let height = "100%";
	export let width = "100%";

	const dispatch = createEventDispatcher<{ change: undefined }>();

	let iframeElement;

	# custom function to update iFrame height on load of HTML
    const onLoad = () => {
		try {
			# calling iFrame document
			const iframeDocument = iframeElement.contentDocument || iframeElement.contentWindow.document;
			# if heigth not custom, setting height individually
			if (height === "100%") {
				# grabbing height from iFrame document
				const height = iframeDocument.documentElement.scrollHeight;
				iframeElement.style.height = `${height}px`;
			}
		} catch (e) {
			console.error("Error accessing iframe content:", e);
		}
	};

	$: value, dispatch("change");
</script>

<div
	class="prose {elem_classes.join(' ')}"
	class:min={min_height}
	class:hide={!visible}
	class:height={height}
>
	# updated to use Iframe instead of HTML, using string values with srcdoc
    <iframe
        bind:this={iframeElement}
        title="iframe component"
        width={width}
        srcdoc={value}
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen
        on:load={onLoad}
    ></iframe>
</div>

<style>
	.min {
		min-height: var(--size-24);
	}
	.hide {
		display: none;
	}
</style>
