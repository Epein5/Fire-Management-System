import 'package:fire_application_1/service/firebasese.dart';
import 'package:fire_application_1/view/firefighter/map.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/material.dart';
// import 'package:cached_network_image/cached_network_image.dart';

class FireFighterView extends StatefulWidget {
  const FireFighterView({super.key});

  @override
  State<FireFighterView> createState() => _FireFighterViewState();
}

class _FireFighterViewState extends State<FireFighterView> {
  FireService fireService = FireService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.redAccent,
        title: const Text(
          'Fire Incidents',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            letterSpacing: 1.2,
          ),
        ),
        centerTitle: true,
        elevation: 0,
      ),
      body: StreamBuilder(
        stream: FirebaseDatabase.instance.ref('Fire').onValue,
        builder: (context, AsyncSnapshot<DatabaseEvent> snapshot) {
          if (!snapshot.hasData) {
            return const Center(
              child: CircularProgressIndicator(
                valueColor: AlwaysStoppedAnimation<Color>(Colors.redAccent),
              ),
            );
          }
          if (snapshot.hasError) {
            return const Center(
              child: Text(
                'Error fetching data',
                style: TextStyle(
                  color: Colors.redAccent,
                  fontWeight: FontWeight.bold,
                ),
              ),
            );
          }

          Map<dynamic, dynamic> fires =
              snapshot.data!.snapshot.value as Map<dynamic, dynamic>;
          List<dynamic> fireList = [];
          fires.forEach((key, value) {
            fireList.add(value);
          });

          return SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  ...fireList.map((fire) {
                    return GestureDetector(
                      onTap: () {
                        print(fire);
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => MapView(
                              fire:
                                  fire, // Pass the fire details as a parameter
                            ),
                          ),
                        );
                      },
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Row(
                                  children: [
                                    Icon(
                                      Icons.whatshot,
                                      color: Colors.redAccent,
                                      size: 28.0,
                                    ),
                                    const SizedBox(width: 8.0),
                                    Text(
                                      'Severity: ${fire['severity']}',
                                      style: TextStyle(
                                        fontSize: 20.0,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.black87,
                                      ),
                                    ),
                                  ],
                                ),
                                TextButton(
                                  onPressed: () {
                                    // fireService.deleteFire(fire['id']);
                                  },
                                  style: TextButton.styleFrom(
                                    foregroundColor: Colors.redAccent,
                                  ),
                                  child: const Text('Delete'),
                                ),
                              ],
                            ),
                            const SizedBox(height: 8.0),
                            Text(
                              'Time Detected: ${fire['time_detected']}',
                              style: const TextStyle(
                                fontSize: 16.0,
                                color: Colors.black87,
                              ),
                            ),
                            const SizedBox(height: 4.0),
                            Text(
                              'Condition: ${fire['condition']}',
                              style: const TextStyle(
                                fontSize: 16.0,
                                color: Colors.black87,
                              ),
                            ),
                            if (fire['condition'] == 'Already Assigned')
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const SizedBox(height: 8.0),
                                  const Text(
                                    'Assigned Vehicles:',
                                    style: TextStyle(
                                      fontSize: 16.0,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.black87,
                                    ),
                                  ),
                                  const SizedBox(height: 4.0),
                                  ...fire['resources_assigned']['vehicles']
                                      .entries
                                      .map(
                                        (vehicle) => Card(
                                          child: ListTile(
                                            leading: CircleAvatar(
                                              backgroundColor: Colors.black,
                                              // child: Image.network(vehicle.value['photo']),
                                            ),
                                            subtitle: Text(
                                              'Number plate :'
                                              ' ${vehicle.key}',
                                              style: const TextStyle(
                                                fontSize: 12.0,
                                                color: Colors.black54,
                                              ),
                                            ),
                                          ),
                                        ),
                                      )
                                      .toList(),
                                  const SizedBox(height: 8.0),
                                  const Text(
                                    'Assigned Manpower:',
                                    style: TextStyle(
                                      fontSize: 16.0,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.black87,
                                    ),
                                  ),
                                  const SizedBox(height: 4.0),
                                  ...fire['resources_assigned']['manpower']
                                      .entries
                                      .map(
                                        (person) => Card(
                                          child: ListTile(
                                            leading: CircleAvatar(
                                              backgroundColor: Colors.black,
                                              // child: Image.network( person.value['photo'])
                                            ),
                                            title: Text(
                                              '${person.value['name']}',
                                              style: const TextStyle(
                                                fontSize: 16.0,
                                                color: Colors.black87,
                                              ),
                                            ),
                                          ),
                                        ),
                                      )
                                      .toList(),
                                ],
                              ),
                            const SizedBox(height: 8.0),
                            Text(
                              'Date Detected: ${fire['date_detected']}',
                              style: const TextStyle(
                                fontSize: 16.0,
                                color: Colors.black87,
                              ),
                            ),
                            const SizedBox(height: 4.0),
                            Text(
                              'Location: ${fire['location']['latitude']}, ${fire['location']['longitude']}',
                              style: const TextStyle(
                                fontSize: 16.0,
                                color: Colors.black87,
                              ),
                            ),
                            const Divider(),
                          ],
                        ),
                      ),
                    );
                  }).toList(),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
