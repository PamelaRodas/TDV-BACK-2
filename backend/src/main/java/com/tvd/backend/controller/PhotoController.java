package com.tvd.backend.controller;

import com.tvd.backend.dto.CreatePhotoMomentRequest;
import com.tvd.backend.model.PhotoMoment;
import com.tvd.backend.service.PhotoMomentService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/photos")
public class PhotoController {

    private final PhotoMomentService photoMomentService;

    public PhotoController(PhotoMomentService photoMomentService) {
        this.photoMomentService = photoMomentService;
    }

    @GetMapping
    public ResponseEntity<List<PhotoMoment>> getPhotoMoments() {
        return ResponseEntity.ok(photoMomentService.getAllMoments());
    }

    @PostMapping
    public ResponseEntity<PhotoMoment> createPhotoMoment(@Valid @RequestBody CreatePhotoMomentRequest request) {
        return ResponseEntity.ok(photoMomentService.addMoment(request));
    }
}
