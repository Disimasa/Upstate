<script>
    import { onMount} from 'svelte';
    import Profile from '../components/Profile.svelte'
    import Tasks from '../components/Tasks.svelte'
    import {url} from '../../static/site_url.js';
    let tasks;
    onMount(fetch_data);
    async function fetch_data() {
        let token = localStorage.getItem('private_token');
        const resp = await fetch(url + 'show/user/private', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'private_token':token})
        });
        const json = await resp.json();
        return json;
    }

</script>
{#await fetch_data()}
    {:then json}
<Profile current_status={json['user']['status']} name={json['user']['name']} surname={json['user']['surname']} job={json['user']['profession']} statuses={json['saved_statuses']}/>
<Tasks tasks={json['tasks']}/>
{/await}