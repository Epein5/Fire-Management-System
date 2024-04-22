import 'package:fire_application_1/components/textfield.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';

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

  @override
  void dispose() {
    super.dispose();
    firstnamecontroller.dispose();
    lastnamecontroller.dispose();
    addresscontroller.dispose();
    phonenumbercontroller.dispose();
    dobcontroller.dispose();
  }

  final picker = ImagePicker();
  File? _image;

  Future<void> _getImage() async {
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

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
                    "Select Fire",
                    style: GoogleFonts.abel(
                      color: Colors.white,
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            Text(
              "Upload a photo of your face",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 16,
                color: Colors.grey[600],
              ),
            ),
            SizedBox(
              height: height * 0.02,
            ),
            SetupTextField(
              controller: firstnamecontroller,
              text: 'First Name',
              icon: Icons.first_page,
            ),
            SetupTextField(
              controller: lastnamecontroller,
              text: 'Last Name',
              icon: Icons.last_page,
            ),
            SetupTextField(
              controller: phonenumbercontroller,
              text: 'Phone Number',
              icon: Icons.phone,
            ),
            SetupTextField(
              controller: addresscontroller,
              text: 'Address',
              icon: Icons.location_city,
            ),
            SetupTextField(
              controller: dobcontroller,
              suffixtext: 'YYYY/MM/DD',
              text: 'DOB',
              icon: Icons.calendar_month,
            ),
            RoundBtn(
              text: "Upload",
              height: height * 0.07,
              width: width * 0.25,
              ontap: () {
                // Add your logic to handle the image upload here
              },
            )
          ],
        ),
      ),
    );
  }
}
