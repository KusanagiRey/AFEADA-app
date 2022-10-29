import 'package:flutter/material.dart';

class ButtonWidget extends StatelessWidget {
  final String text;
  final VoidCallback onClicked;

  const ButtonWidget({
    Key? key,
    required this.text,
    required this.onClicked,
}): super(key: key);

  @override
  Widget build(BuildContext context) => ElevatedButton(
    style: ElevatedButton.styleFrom(
      backgroundColor: Color(0xff423C63),
      shape: StadiumBorder(),
      onPrimary: Color(0xffE6E6FA),

    ),
    child: Text(text),
    onPressed: onClicked,
  );
}