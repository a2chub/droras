import firebase from 'firebase'

if (!firebase.apps.length) {
  firebase.initializeApp({
    apiKey: 'AIzaSyDJLakGhgbVQhgu-AlF7_JP36KYZlOE8i8',
    authDomain: 'jdl-main.firebaseapp.com',
    databaseURL: 'https://jdl-main.firebaseio.com',
    projectId: 'jdl-main',
    storageBucket: 'jdl-main.appspot.com',
    messagingSenderId: '457977284384',
    appId: '1:457977284384:web:bdfa2434119cb460043945'
  })
}

export default firebase
