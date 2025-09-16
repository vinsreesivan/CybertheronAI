/* global Office */
async function onMessageReadHandler(event) {
  const item = Office.context.mailbox.item;
  const body = await new Promise(r => item.body.getAsync('text', res => r(res.value || '')));
  const resp = await fetch('https://localhost:8080/analyze', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({text: body}) });
  const json = await resp.json();
  item.notificationMessages.replaceAsync('aiLabelBanner', { type: Office.MailboxEnums.ItemNotificationMessageType.InformationalMessage, message:   (Conf %), persistent: true }, () => event.completed());
}
if (typeof window !== 'undefined') window.onMessageReadHandler = onMessageReadHandler;
