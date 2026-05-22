package com.tvd.backend.controller;

import com.tvd.backend.repository.DiaryEntryRepository;
import com.tvd.backend.repository.PhotoMomentRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/content")
public class ContentController {

    private final DiaryEntryRepository diaryEntryRepository;
    private final PhotoMomentRepository photoMomentRepository;

    public ContentController(DiaryEntryRepository diaryEntryRepository, PhotoMomentRepository photoMomentRepository) {
        this.diaryEntryRepository = diaryEntryRepository;
        this.photoMomentRepository = photoMomentRepository;
    }

    @GetMapping("/summary")
    public ResponseEntity<Map<String, Long>> getContentSummary() {
        Map<String, Long> summary = new HashMap<>();
        summary.put("diaryCount", diaryEntryRepository.count());
        summary.put("photoCount", photoMomentRepository.count());
        return ResponseEntity.ok(summary);
    }
}
