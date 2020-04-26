<svelte:head>
    <title>Hello from UniBots!</title>
</svelte:head>
<script>
    import lottie from 'lottie-web'
    import {onMount} from 'svelte'

    let svgContainer;
    onMount(() => {
        let animItem = lottie.loadAnimation({
            container: svgContainer,
            animType: 'svg',
            loop: true,
            path: 'animation.json'
        });
    });
</script>

<main>
    <div class='Anim' bind:this={svgContainer}></div>
    <div class="Text">
        <h1>Hello!</h1>
        <h3>If you see this, it means that your <a href="https://example.com/">UniBots</a> server works!
            Check <a href="https://example.com/">docs</a> to get info, how to make it working on Yandex Dialogs, VK and
            Telegram</h3>
    </div>
</main>
<style>
    @import url('https://fonts.googleapis.com/css?family=Comic+Neue&display=swap');
    main {
        margin: 20vh auto;
        padding: 4em;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        max-width: 800px;
    }

    h1 {
        color: #ff7070;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
    }

    h3 {
        font-size: 1.5em;
        font-weight: normal;
        color: darkgrey;
        font-family: 'Comic Neue', cursive, sans-serif;
    }
    .Anim {
        width: 30%;
        height: 30%;
        min-width: 200px;
        min-height: 200px;
        max-width: 300px;
        max-height: 300px;
    }
    .Text {
        width: 70%;
        padding-left: 2em;
        padding-bottom: 4em;
    }

</style>