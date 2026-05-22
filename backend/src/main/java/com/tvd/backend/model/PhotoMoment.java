package com.tvd.backend.model;

public class PhotoMoment {
    private final String id;
    private String image;
    private String caption;
    private String author;

    public PhotoMoment(String id, String image, String caption, String author) {
        this.id = id;
        this.image = image;
        this.caption = caption;
        this.author = author;
    }

    public String getId() {
        return id;
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
