import firebase from 'firebase/app'
import 'firebase/firestore'

if (!firebase.apps.length) {
  firebase.initializeApp({
    projectId: 'jdl-main',
    apiKey: 'AIzaSyDJLakGhgbVQhgu-AlF7_JP36KYZlOE8i8'
  })
}

export default firebase
