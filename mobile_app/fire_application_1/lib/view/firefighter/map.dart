import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:http/http.dart' as http;
import 'package:latlong2/latlong.dart';

class MapView extends StatefulWidget {
  final Map<dynamic, dynamic> fire;
  const MapView({Key? key, required this.fire}) : super(key: key);

  @override
  _MapViewState createState() => _MapViewState();
}

class _MapViewState extends State<MapView> {
  List<LatLng> polylineCoordinates = [];

  @override
  void initState() {
    super.initState();
    _drawRoute();
  }

  void _drawRoute() async {
    // Specify the starting location (27.670572, 85.420738)
    //TIA FIre Stattion 
    LatLng startLocation = LatLng(27.695209212296703, 85.35959313206881);

    // Specify the destination location (fire location)
    LatLng endLocation = LatLng(
      widget.fire['location']['latitude'],
      widget.fire['location']['longitude'],
    );

    // Get the polyline coordinates from the Open Route Service API
    polylineCoordinates = await _getPolylineCoordinates(
      startLocation,
      endLocation,
    );

    setState(() {});
  }

  Future<List<LatLng>> _getPolylineCoordinates(
    LatLng startLocation,
    LatLng endLocation,
  ) async {
    // Construct the API request URL
    String apiUrl =
        'https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf62483e48505671d7423b8e8233754651b092&start=${startLocation.longitude},${startLocation.latitude}&end=${endLocation.longitude},${endLocation.latitude}';

    // Make the HTTP request
    final response = await http.get(Uri.parse(apiUrl));

    // Check if the request was successful
    if (response.statusCode == 200) {
      // Parse the response data
      final data = jsonDecode(response.body);
      print(data['location']);
      // Extract the route coordinates from the response
      final List<dynamic> coordinates =
          data['features'][0]['geometry']['coordinates'];

      // Convert the coordinates to LatLng objects
      return coordinates.map((coord) => LatLng(coord[1], coord[0])).toList();
    } else {
      // Handle the error case
      throw Exception('Failed to get route coordinates');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('MapView'),
      ),
      body: FlutterMap(
        options: MapOptions(
          initialCenter: LatLng(
            widget.fire['location']['latitude'],
            widget.fire['location']['longitude'],
          ),
          initialZoom: 13.0,
        ),
        children: [
          TileLayer(
            urlTemplate: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            subdomains: const ['a', 'b', 'c'],
          ),
          PolylineLayer(
            polylines: [
              Polyline(
                points: polylineCoordinates,
                strokeWidth: 4.0,
                color: Colors.blue,
              ),
            ],
          ),
          MarkerLayer(
            markers: [
              Marker(
                point: LatLng(
                  widget.fire['location']['latitude'],
                  widget.fire['location']['longitude'],
                ),
                width: 80.0,
                height: 80.0,
                child: const Icon(
                  Icons.fire_truck,
                  color: Colors.red,
                  size: 40.0,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
