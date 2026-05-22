package com.tvd.backend.dto;

import jakarta.validation.constraints.NotBlank;

public class CreatePhotoMomentRequest {
    @NotBlank(message = "image is required")
    private String image;

    @NotBlank(message = "caption is required")
    private String caption;

    private String author;

    public CreatePhotoMomentRequest() {
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }

    public String getCaption() {
        return caption;
    }

    public void setCaption(String caption) {
        this.caption = caption;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }
}
