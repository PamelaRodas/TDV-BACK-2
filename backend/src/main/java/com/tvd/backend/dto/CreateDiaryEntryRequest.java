package com.tvd.backend.dto;

import jakarta.validation.constraints.NotBlank;

public class CreateDiaryEntryRequest {
    @NotBlank(message = "title is required")
    private String title;

    @NotBlank(message = "text is required")
    private String text;

    @NotBlank(message = "label is required")
    private String label;

    private String author;

    public CreateDiaryEntryRequest() {
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }
}
