package com.example;

import java.util.HashMap;
import java.util.Map;

public class App {
    public static void main(String[] args) {
        Map<String, String> response = new HashMap<>();
        response.put("message", "WEBHOOK арқылы автоматты іске қосу!");

        System.out.println(response);
    }
}
