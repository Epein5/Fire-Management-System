// firebasese.dart
import 'package:firebase_database/firebase_database.dart';
import 'package:location/location.dart';

class FireService {
  final databaseReference = FirebaseDatabase.instance.ref();

  Future<void> addFire(String severity, LocationData locationData) async {
    await databaseReference.child('Fire').push().set({
      'severity': severity,
      'location': {
        'latitude': locationData.latitude,
        'longitude': locationData.longitude,
      },
      'condition': 'Not Assigned',
      'date_detected': DateTime.now().toIso8601String().substring(0, 10),
      'time_detected': '${DateTime.now().toIso8601String().substring(0, 10)} ${DateTime.now().toIso8601String().substring(11, 16)}',
    });
  }
}
