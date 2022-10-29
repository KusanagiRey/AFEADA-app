import 'package:flutter/material.dart';
import 'package:afeada/pages/news.dart';
import 'package:afeada/pages/profile.dart';
import 'package:afeada/pages/calendar.dart';

void main() => runApp(MaterialApp(
  title: 'AFEADA',
  theme: ThemeData(
    primarySwatch: Colors.blue,
  ),
  initialRoute: '/',
  routes: {
    '/': (context) => const News(),
    '/profile': (context) => const Profile(),
    '/calendar': (context) => const Calendar(),
  },
  )
);