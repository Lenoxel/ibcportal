function aoEnviarFormulario(e) {
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

  // Lançar erro faz o Google te avisar por email (configure em Gatilhos > Notificações de falha)
  if (resp.getResponseCode() >= 300) {
    throw new Error(`API respondeu ${resp.getResponseCode()}: ${resp.getContentText()}`);
  }
}