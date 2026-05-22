package com.tvd.backend.controller;

import com.tvd.backend.dto.CreateDiaryEntryRequest;
import com.tvd.backend.model.DiaryEntry;
import com.tvd.backend.service.DiaryEntryService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/diary")
public class DiaryController {

    private final DiaryEntryService diaryEntryService;

    public DiaryController(DiaryEntryService diaryEntryService) {
        this.diaryEntryService = diaryEntryService;
    }

    @GetMapping
    public ResponseEntity<List<DiaryEntry>> getDiaryEntries() {
        return ResponseEntity.ok(diaryEntryService.getAllEntries());
    }

    @PostMapping
    public ResponseEntity<DiaryEntry> createDiaryEntry(@Valid @RequestBody CreateDiaryEntryRequest request) {
        return ResponseEntity.ok(diaryEntryService.addEntry(request));
    }
}
