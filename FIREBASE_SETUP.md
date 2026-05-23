# Firebase Setup

This version uses Firestore only. Firebase Storage is not required.

## 1. Enable Authentication

The screenshot error `auth/configuration-not-found` means Firebase Authentication is not enabled/configured for this project.

Open Firebase Console:

1. Go to Authentication.
2. Click Get started if it asks.
3. Open Sign-in method.
4. Enable Email/Password.

## 2. Replace the deny-all Firestore rules

Deploy or paste `firestore.rules` into Firebase Console > Firestore Database > Rules.

Your current rule blocks every app feature:

```js
match /{document=**} {
  allow read, write: if false;
}
```

## 3. Create the first admin

Default bootstrap admin:

```txt
Email: admin@diuqbank.local
Password: Admin@123456
```

You can change this later in Admin Panel > User & Admin Manager. The bootstrap account works locally so you can reach the admin panel even before Firebase is fully configured.

For synced Firebase admin access, admin access is:

1. A Firebase Authentication email/password account.
2. A Firestore document at `users/{uid}` with:

```json
{
  "email": "admin@example.com",
  "role": "admin"
}
```

Get the `uid` from Firebase Console > Authentication > Users.

If you enable Email/Password Authentication and create/sign up `admin@diuqbank.local`, the app will create its Firestore user role as `admin` automatically after you deploy `firestore.rules`.

## 4. Firestore-only uploads

Uploaded PDFs/images are saved in:

- `uploads/{uploadId}`
- `uploads/{uploadId}/chunks/{chunkId}`

Submissions and approved papers store a reference like:

```txt
firestore://uploads/uploadId
```

## 5. Deploy with Firebase CLI

```powershell
firebase login
firebase use diu-ai
firebase deploy --only firestore:rules
```

If you do not use the CLI, paste `firestore.rules` manually in Firebase Console.
