<script>
    import { onMount} from 'svelte';
    import Profile from '../components/Profile.svelte'
    import Tasks from '../components/Tasks.svelte'
    import {url} from '../../static/site_url.js';
    onMount(fetch_data);
    async function fetch_data() {
        let token = localStorage.getItem('public_token');
        const resp = await fetch(url + 'show/user?' + new URLSearchParams({'public_token': token}));
        const json = await resp.json();
        return json;
    }

</script>
{#await fetch_data()}
    {:then json}
<Profile current_status={json['user']['status']} name={json['user']['name']} surname={json['user']['surname']} job={json['user']['profession']} />
<Tasks tasks={json['tasks']}/>
{/await}