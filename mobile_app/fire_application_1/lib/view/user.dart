import 'package:fire_application_1/components/popupmessages.dart';
import 'package:fire_application_1/components/textfield.dart';
import 'package:fire_application_1/service/firebasese.dart';
import 'package:flutter/material.dart';
import 'package:flutter_tflite/flutter_tflite.dart';
import 'package:google_fonts/google_fonts.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:location/location.dart';
import 'package:dropdown_button2/dropdown_button2.dart';

class UserView extends StatefulWidget {
  const UserView({super.key});

  @override
  State<UserView> createState() => _UserViewState();
}

class _UserViewState extends State<UserView> {
  TextEditingController firstnamecontroller = TextEditingController();
  TextEditingController lastnamecontroller = TextEditingController();
  TextEditingController addresscontroller = TextEditingController();
  TextEditingController phonenumbercontroller = TextEditingController();
  TextEditingController dobcontroller = TextEditingController();

  Location location = Location();
  LocationData? _locationData;
  FireService fireservice = FireService();
  PopUpMessages popupmessages = PopUpMessages();

  @override
  void initState() {
    super.initState();
    loadmodel();
    _image = null; // Initialize _image with null
  }

  detect_image(File? image) async {
    if (image != null) {
      var prediction = await Tflite.runModelOnImage(
          path: image.path,
          numResults: 4,
          threshold: 0.001,
          imageMean: 127.5,
          imageStd: 127.5);

      setState(() {
        _loading = false;
        _predictions = prediction!;
        print(_predictions);
      });
    }
  }

  bool _loading = true;
  late File? _image;
  List _predictions = [];
  final picker = ImagePicker();

  loadmodel() async {
    await Tflite.loadModel(
        model: 'assets/model.tflite', labels: 'assets/text.txt');
  }

  @override
  void dispose() {
    super.dispose();
    firstnamecontroller.dispose();
    lastnamecontroller.dispose();
    addresscontroller.dispose();
    phonenumbercontroller.dispose();
    dobcontroller.dispose();
  }

  Future<void> _getImage() async {
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
      detect_image(_image);
    }
  }

  Future<void> _getimagefromcamera() async {
    final pickedFile = await picker.pickImage(source: ImageSource.camera);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
      detect_image(_image);
    }
  }

  Future<LocationData?> retrieveLocation() async {
    bool _serviceEnabled;
    PermissionStatus _permissionGranted;

    _serviceEnabled = await location.serviceEnabled();
    if (!_serviceEnabled) {
      _serviceEnabled = await location.requestService();
      if (!_serviceEnabled) {
        print('Location services are disabled.');
        return null;
      }
    }

    _permissionGranted = await location.hasPermission();
    if (_permissionGranted == PermissionStatus.denied) {
      _permissionGranted = await location.requestPermission();
      if (_permissionGranted != PermissionStatus.granted) {
        print('Location permission denied.');
        return null;
      }
    }

    _locationData = await location.getLocation();
    setState(() {
      _locationData = _locationData;
    });
    return _locationData;
  }

  final List<String> items = [
    'High',
    'Midium',
    'Low',
  ];
  String? selectedValue;
  String? selectedValue2;

  @override
  Widget build(BuildContext context) {
    final height = MediaQuery.of(context).size.height;
    final width = MediaQuery.of(context).size.width;
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            Stack(
              children: [
                Container(
                  height: height * 0.35,
                  decoration: const BoxDecoration(
                    color: Color.fromARGB(255, 255, 255, 255),
                  ),
                ),
                Container(
                  height: height * 0.3,
                  decoration: const BoxDecoration(
                    color: Color.fromARGB(224, 187, 50, 0),
                    borderRadius: BorderRadius.only(
                      bottomLeft: Radius.circular(175),
                    ),
                  ),
                ),
                Align(
                  heightFactor: 1.6,
                  alignment: Alignment.bottomCenter,
                  child: GestureDetector(
                    onTap: _getImage,
                    child: Container(
                      height: height * 0.3,
                      width: width * 0.8,
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(30),
                      ),
                      child: _image != null
                          ? ClipRRect(
                              borderRadius: BorderRadius.circular(60),
                              child: Padding(
                                padding: const EdgeInsets.all(8.0),
                                child: Image.file(
                                  _image!,
                                  fit: BoxFit.cover,
                                ),
                              ),
                            )
                          : Container(),
                    ),
                  ),
                ),
                Align(
                  heightFactor: 5,
                  alignment: Alignment.center,
                  child: Text(
                    "Report Fire in Your Area ",
                    style: GoogleFonts.satisfy(
                      color: Colors.white,
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            _loading == true
                ? Text(
                    "Select Picture or",
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                      color: Colors.grey[600],
                    ),
                  )
                : Divider(),
            _loading == true
                ? GestureDetector(
                    onTap: _getimagefromcamera,
                    child: const Text(
                      "CLICK HERE TO CLICK PICTURE",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                        color: Color.fromARGB(121, 43, 89, 117),
                      ),
                    ),
                  )
                : _predictions.isNotEmpty
                    ? Text(
                        'Confidence ${(_predictions[0]['confidence'] * 100).toString()}.% ${_predictions[0]['label'].toString().substring(1)}')
                    : Container(),
            SizedBox(
              height: height * 0.02,
            ),
            // SetupTextField(
            //   controller: firstnamecontroller,
            //   text: 'First Name',
            //   icon: Icons.first_page,
            // ),
            SizedBox(
              width: MediaQuery.of(context).size.width *
                  0.9, // 80% of screen width
              child: DropdownButtonHideUnderline(
                child: DropdownButton2<String>(
                  // isExpanded: true,
                  hint: Text(
                    'Select The Severity of Fire',
                    style: TextStyle(
                      fontSize: 14,
                      color: Theme.of(context).hintColor,
                    ),
                  ),
                  items: items
                      .map((String item) => DropdownMenuItem<String>(
                            value: item,
                            child: Text(
                              item,
                              style: const TextStyle(
                                fontSize: 14,
                              ),
                            ),
                          ))
                      .toList(),
                  value: selectedValue,
                  onChanged: (String? value) {
                    setState(() {
                      selectedValue = value;
                    });
                  },
                  buttonStyleData: ButtonStyleData(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.all(Radius.circular(8.0)),
                      border: Border.all(
                        color: Colors.grey,
                        width: 1.0,
                      ),
                    ),
                    padding: EdgeInsets.symmetric(horizontal: 16),
                    height: 40,
                  ),
                  menuItemStyleData: const MenuItemStyleData(
                    height: 40,
                  ),
                ),
              ),
            ),
            SizedBox(
              height: height * 0.02,
            ),
            // SizedBox(
            //   width: MediaQuery.of(context).size.width *
            //       0.9, // 80% of screen width
            //   child: DropdownButtonHideUnderline(
            //     child: DropdownButton2<String>(
            //       // isExpanded: true,
            //       hint: Text(
            //         'Fire Type',
            //         style: TextStyle(
            //           fontSize: 14,
            //           color: Theme.of(context).hintColor,
            //         ),
            //       ),
            //       items: items
            //           .map((String item) => DropdownMenuItem<String>(
            //                 value: item,
            //                 child: Text(
            //                   item,
            //                   style: const TextStyle(
            //                     fontSize: 14,
            //                   ),
            //                 ),
            //               ))
            //           .toList(),
            //       value: selectedValue2,
            //       onChanged: (String? value) {
            //         setState(() {
            //           selectedValue = value;
            //         });
            //       },
            //       buttonStyleData: ButtonStyleData(
            //         decoration: BoxDecoration(
            //           borderRadius: BorderRadius.all(Radius.circular(8.0)),
            //           border: Border.all(
            //             color: Colors.grey,
            //             width: 1.0,
            //           ),
            //         ),
            //         padding: EdgeInsets.symmetric(horizontal: 16),
            //         height: 40,
            //       ),
            //       menuItemStyleData: const MenuItemStyleData(
            //         height: 40,
            //       ),
            //     ),
            //   ),
            // ),
            SizedBox(
              height: height * 0.02,
            ),
            selectedValue != null &&
                    _predictions[0]['label'].toString().substring(1) == ' fire'
                ? RoundBtn(
                    text: "Send Report",
                    height: height * 0.07,
                    width: width * 0.5,
                    ontap: () async {
                      LocationData? locationData = await retrieveLocation();
                      if (locationData != null) {
                        fireservice
                            .addFire(selectedValue!, locationData)
                            .then((value) {
                          Navigator.pop(context);
                          popupmessages.flushBarErrorMessage(
                              'Fire Reported Successfully', context);
                        });
                      }
                    },
                  )
                : Container(),
          ],
        ),
      ),
    );
  }
}
