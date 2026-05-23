# Secure Firebase Login Setup

This is for the live GitHub Pages site:

https://mrwhoistheboss1111.github.io/InfinityWord/

The website does not store any admin password, admin email list, or editable admin secret in `index.html`.

Firebase Authentication handles global login from any device. Admin access is decided by Firebase custom claims (`admin: true`, `mainAdmin: true`), which can only be set with Firebase Admin credentials.

## 1. Enable Firebase Authentication

In Firebase Console:

1. Open project `diu-ai`.
2. Go to Authentication.
3. Enable Google sign-in.
4. Enable Email/Password sign-in if you want password login.
5. Go to Authentication > Settings > Authorized domains.
6. Add `mrwhoistheboss1111.github.io`.

## 2. Publish Firestore Rules

Paste `firestore.rules` into Firebase Console > Firestore Database > Rules, then click Publish.

These rules only allow admin edits when the signed-in Firebase token has `admin: true`. Only the main admin token can create/delete user records.

## 3. Install Admin Script Dependencies

From this repo folder:

```powershell
npm.cmd install
```

## 4. Add Private Service Account Key

Firebase Console:

1. Project settings.
2. Service accounts.
3. Generate new private key.
4. Download the JSON.
5. Rename it to `serviceAccountKey.json`.
6. Put it in this repo folder while running admin scripts.

Never upload `serviceAccountKey.json` to GitHub.

## 5. Make Yourself Main Admin

```powershell
npm.cmd run set-main-admin -- asrahi2007@gmail.com
```

Then sign out of the website and sign in again.

## 6. Add Email/Password Users

```powershell
npm.cmd run create-login-user -- student@example.com
```

That user can log in, but cannot edit admin-only data.
