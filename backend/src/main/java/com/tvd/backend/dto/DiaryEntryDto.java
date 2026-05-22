package com.tvd.backend.dto;

public class DiaryEntryDto {
    private String id;
    private String title;
    private String text;
    private String label;
    private String author;

    public DiaryEntryDto() {
    }

    public DiaryEntryDto(String id, String title, String text, String label, String author) {
        this.id = id;
        this.title = title;
        this.text = text;
        this.label = label;
        this.author = author;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
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
