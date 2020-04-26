<script>
    import {url} from '../../static/site_url.js';
async function Create_team() {
let cookie_public = get_cookie('public_token');
if (cookie_public === null) {
    const resp = await fetch(url + 'create/user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'platform_id': document.documentElement.clientWidth+' '+document.documentElement.clientHeight,
        'platform_name':'web', 'name':'', 'surname':''})
    });
    const json = await resp.json();
    alert(json['user']['name']);
}
}
function get_cookie(cookie_name)
{
  let results = document.cookie.match('(^|;) ?' + cookie_name + '=([^;]*)(;|$)');

  if (results)
    return (unescape(results[2]));
  else
    return null;
}
</script>
<style>
.create_team {
    margin-top: 200px;
}
</style>
<button class="create_team" on:click={Create_team}>Создать команду</button>