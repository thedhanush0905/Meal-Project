package com.example.backend.controller;

import com.example.backend.dto.AIQueryRequest;
import com.example.backend.dto.AIQueryResponse;
import com.example.backend.service.AIService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class AIController {
    
    private final AIService aiService;
    
    @PostMapping("/query")
    public ResponseEntity<AIQueryResponse> queryAI(@Valid @RequestBody AIQueryRequest request) {
        try {
            AIQueryResponse response = aiService.queryAI(request.getQuery());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                    .body(new AIQueryResponse("Failed to process your query. Please try again.", request.getQuery()));
        }
    }
}
