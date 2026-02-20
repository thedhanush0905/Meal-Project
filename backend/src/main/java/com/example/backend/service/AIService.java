package com.example.backend.service;

import com.example.backend.dto.AIQueryResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Map;

@Service
public class AIService {
    
    private final WebClient webClient;
    
    @Value("${ai.service.url:http://localhost:8001}")
    private String aiServiceUrl;
    
    public AIService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.build();
    }
    
    @SuppressWarnings("unchecked")
    public AIQueryResponse queryAI(String query) {
        try {
            Map<String, String> request = Map.of("query", query);
            
            Map<String, Object> response = webClient.post()
                    .uri(aiServiceUrl + "/api/ai/query")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
            
            if (response != null && response.containsKey("response")) {
                return new AIQueryResponse(
                    (String) response.get("response"),
                    query
                );
            }
            
            throw new RuntimeException("Invalid response from AI service");
        } catch (Exception e) {
            throw new RuntimeException("Failed to query AI service: " + e.getMessage(), e);
        }
    }
}
