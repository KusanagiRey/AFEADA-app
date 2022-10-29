import 'package:flutter/material.dart';

class AboutNew extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      width: 300,
      height: 180,
      decoration: BoxDecoration(
        color: Colors.grey,
        borderRadius: BorderRadius.circular(15)
      ),
      child: Column (
        children: [
          SizedBox(height: 20),
          Text(
            'Первая Новость',
            style: TextStyle(
              fontSize: 30,
              color: Colors.black,
              fontWeight: FontWeight.w600,
            ),
          ),
         /* SizedBox(height: 10),
          Container(
            padding: EdgeInsets.all(10),
            child: Text(
              'Текст новости',
              style: TextStyle(fontSize: 12, color: Colors.black,
                fontWeight: FontWeight.w600,
              ),
            ),*/
            SizedBox(height: 10),
            Container(
              child: Text(
                'Очень хорошая новость о том что все работает',
                    style:TextStyle(fontSize: 12, color: Colors.black),
              ),
            )
         // )
        ],
      ),
    );
  }
}