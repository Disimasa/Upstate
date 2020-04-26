<script context="module">
    import Profile from '../components/Profile.svelte'
    import Tasks from '../components/Tasks.svelte'
    import {url} from '../../static/site_url.js';
    export async function preload({ params, query }) {
    const resp = await this.fetch(url + 'show/user?' + new URLSearchParams({public_token: 'public:fea6498adf03231d71db0035f4bb7774adaa99b22c5846d04252a3f576900e1b'}));
    const json = await resp.json();
    return {json};
}
</script>
<script>
    export let json;
</script>
<Profile current_status={json['status']} name={json['name']} surname={json['surname']} job={json['profession']} />
<Tasks/>