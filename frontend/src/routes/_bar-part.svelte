<script>
    export let title;
    export let width;
    export let color;
</script>

<div style="--barcolor: {color}; --barwidth: {width}">{title}</div>

<style>
    div {
        background-color: var(--barcolor);
        width: var(--barwidth);
    }
</style>