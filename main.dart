import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:google_fonts/google_fonts.dart';

void main() {
  runApp(PerformanceCheckApp());
}

class PerformanceCheckApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Performance Check',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        textTheme: GoogleFonts.poppinsTextTheme(),
      ),
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _timingController = TextEditingController();
  String _responseMessage = '';
  Map<String, dynamic>? _performanceData;
  List<dynamic>? _improvementTips;

  final String apiBaseUrl = 'http://127.0.0.1:8000'; // Change to your backend URL

  Future<void> addRaceResult() async {
    final url = Uri.parse('$apiBaseUrl/add_race_result');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': _nameController.text,
        'timing': double.tryParse(_timingController.text),
      }),
    );

    if (response.statusCode == 200) {
      final responseData = jsonDecode(response.body);
      setState(() {
        _responseMessage = responseData['message'] ?? 'Race result added.';
        _improvementTips = responseData['tips'] ?? [];
      });
    } else {
      setState(() {
        _responseMessage = jsonDecode(response.body)['detail'] ?? 'An error occurred.';
      });
    }
  }

  Future<void> viewPerformance() async {
    final url = Uri.parse('$apiBaseUrl/view_performance/${_nameController.text}');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      setState(() {
        _performanceData = jsonDecode(response.body);
      });
    } else {
      setState(() {
        _responseMessage = jsonDecode(response.body)['detail'] ?? 'An error occurred.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Performance Check'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _nameController,
              decoration: InputDecoration(labelText: 'Name'),
            ),
            TextField(
              controller: _timingController,
              decoration: InputDecoration(labelText: 'Timing'),
              keyboardType: TextInputType.number,
            ),
            SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                ElevatedButton(
                  onPressed: addRaceResult,
                  child: Text('Add Result'),
                ),
                ElevatedButton(
                  onPressed: viewPerformance,
                  child: Text('View Performance'),
                ),
              ],
            ),
            SizedBox(height: 16),
            if (_responseMessage.isNotEmpty) Text(_responseMessage),
            if (_improvementTips != null && _improvementTips!.isNotEmpty) ...[
              Text('Improvement Tips:', style: TextStyle(fontWeight: FontWeight.bold)),
              ..._improvementTips!.map((tip) => Text('- $tip')).toList(),
            ],
            if (_performanceData != null) ...[
              Text('Name: ${_performanceData!['name']}'),
              Text('Total Races: ${_performanceData!['total_races']}'),
              Text('Average Timing: ${_performanceData!['average_timing']}'),
              Text('Below Threshold: ${_performanceData!['below_threshold']}'),
              Text('Above Threshold: ${_performanceData!['above_threshold']}'),
              SizedBox(height: 16),
              Text('Details:'),
              Expanded(
                child: ListView.builder(
                  itemCount: _performanceData!['details'].length,
                  itemBuilder: (context, index) {
                    final race = _performanceData!['details'][index];
                    return ListTile(
                      title: Text('Race ${index + 1}'),
                      subtitle: Text(
                          'Timing: ${race['timing']}, Status: ${race['status']}, Level: ${race['level']}'),
                    );
                  },
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
