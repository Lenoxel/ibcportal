function onMemberRegisterFormSubmit(e) {
  const props = PropertiesService.getScriptProperties();

  const data = {};
  e.response.getItemResponses().forEach(r => {
    data[r.getItem().getTitle()] = r.getResponse();
  });

  const resp = UrlFetchApp.fetch(props.getProperty('API_URL'), {
    method: 'post',
    contentType: 'application/json',
    headers: { 'X-Webhook-Secret': props.getProperty('API_SECRET') },
    payload: JSON.stringify({ data }),
    muteHttpExceptions: true,
  });

  const respContent = resp.getContentText();
  const respCode = resp.getResponseCode();

  console.log(`API respondeu ${respCode}: ${respContent}`);

  if (respCode >= 300) {
    throw new Error(`API respondeu ${respCode}: ${respContent}`);
  }
}