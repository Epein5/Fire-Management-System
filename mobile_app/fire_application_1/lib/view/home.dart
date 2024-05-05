import 'package:fire_application_1/components/textfield.dart';
import 'package:fire_application_1/view/firefighter/1.dart';
import 'package:fire_application_1/view/user.dart';
import 'package:flutter/material.dart';

class HomeView extends StatelessWidget {
  const HomeView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          ElevatedButton(
            onPressed: () {
              Navigator.push(context,
                  MaterialPageRoute(builder: (context) => const UserView()));
            },
            child: const Text('User'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => const FireFighterView()));
            },
            child: const Text('Firefighter'),
          ),
          const FlutterWidget()
        ],
      ),
    ));
  }
}
