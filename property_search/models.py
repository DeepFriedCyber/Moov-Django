# property_search/models.py

from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.name}, {self.city}"

class PropertyType(models.Model):
    name = models.CharField(max_length=50)  # e.g., House, Flat, Bungalow
    
    def __str__(self):
        return self.name

class Property(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    has_garden = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    square_feet = models.PositiveIntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    date_listed = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Properties"
    
    def __str__(self):
        return f"{self.title} - £{self.price}"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Image for {self.property.title}"

class SearchQuery(models.Model):
    query_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    extracted_params = models.JSONField(null=True, blank=True)
    result_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Search Queries"
    
    def __str__(self):
        return f"{self.query_text[:50]}... ({self.result_count} results)"