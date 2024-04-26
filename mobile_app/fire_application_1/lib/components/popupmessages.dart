// import 'package:flutter/material.dart';
import 'package:another_flushbar/flushbar.dart';
import 'package:another_flushbar/flushbar_route.dart';
import 'package:flutter/material.dart';
// import 'package:fluttertoast/fluttertoast.dart';
// import 'package:another_flushbar/flushbar_route.dart';

class PopUpMessages {

   void flushBarErrorMessage(String message, BuildContext context) {
    showFlushbar(
        context: context,
        flushbar: Flushbar(
          flushbarPosition: FlushbarPosition.BOTTOM,
          icon: const Icon(
            Icons.error,
            color: Colors.white,
          ),
          duration: const Duration(seconds: 5),
          reverseAnimationCurve: Curves.decelerate,
          borderRadius: BorderRadius.circular(10),
          forwardAnimationCurve: Curves.decelerate,
          margin: const EdgeInsets.all(10),
          padding: const EdgeInsets.all(10),
          message: message,
          backgroundColor: Colors.red,
        )..show(context));
  }


}