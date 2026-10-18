function onMemberRegisterFormSubmit(e) {
  const props = PropertiesService.getScriptProperties();

  const data = {};
  e.response.getItemResponses().forEach(r => {
    data[r.getItem().getTitle()] = r.getResponse();
  });

  const photoIds = data['Foto'] || [];
  const photos = (Array.isArray(photoIds) ? photoIds : [photoIds])
    .filter(Boolean)
    .map(id => {
      const file = DriveApp.getFileById(id);
      const blob = file.getBlob();

      return {
        filename: file.getName(),
        contentType: blob.getContentType(),
        base64: Utilities.base64Encode(blob.getBytes()),
      };
    });

  const resp = UrlFetchApp.fetch(props.getProperty('API_URL'), {
    method: 'post',
    contentType: 'application/json',
    headers: { 'X-Webhook-Secret': props.getProperty('API_SECRET') },
    payload: JSON.stringify({ data, photos }),
    muteHttpExceptions: true,
  });

  const respContent = resp.getContentText();
  const respCode = resp.getResponseCode();

  console.log(`API respondeu ${respCode}: ${respContent}`);

  if (respCode >= 300) {
    throw new Error(`API respondeu ${respCode}: ${respContent}`);
  }
}