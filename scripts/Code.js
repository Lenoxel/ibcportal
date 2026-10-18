function setupMemberRegisterTrigger() {
  const props = PropertiesService.getScriptProperties();
  const googleFormId = props.getProperty('GOOGLE_FORM_ID');

    if (!googleFormId) {
        throw new Error('Google Form ID não está definido nas propriedades do script.');
    }

  const form = FormApp.openById(googleFormId);
  const handler = 'onMemberRegisterFormSubmit';

  const alreadyExists = ScriptApp.getProjectTriggers().some(trigger =>
    trigger.getHandlerFunction() === handler &&
    trigger.getEventType() === ScriptApp.EventType.ON_FORM_SUBMIT &&
    trigger.getTriggerSourceId() === form.getId()
  );

  if (!alreadyExists) {
    ScriptApp.newTrigger(handler)
      .forForm(form)
      .onFormSubmit()
      .create();
  }
}

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