# Vuo
## Share photostreams with a passphrase

### Features
- User login
- Logged in users can create their stream with passphrase (eg. platform.com/feed/< passphrase >)
- Anyone knowing the passphrase can view created stream without login
- Logged in users can upload and give upvotes to photos on any stream

### Considerations
- [ ] Light [Preact](https://preactjs.com/) front to render feeds & update live
- [ ] [Ably](https://www.ably.io/) integration to get feed updates in real time
- [ ] Require [reCAPTCHA](https://www.google.com/recaptcha/about/) on auth & upload forms.
- [ ] Let feed owner disable uploads
- [ ] Hide guest uploads from public feed
