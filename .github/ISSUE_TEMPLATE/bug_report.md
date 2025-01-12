---
name: Bug report
about: Create a report to help us improve
title: Improper User Validation in for_user Method Leads to Unauthorized Access
labels: bug
assignees: XusanDev07

---

### **Describe the bug**
In the `djangorestframework-simplejwt` library version [affected version], the `for_user` method does not properly validate the user before allowing access to resources. As a result, users whose accounts are disabled can still access protected resources, leading to information disclosure.

### **To Reproduce**
Steps to reproduce the behavior:
1. Install `djangorestframework-simplejwt` version [affected version].
2. Create a user account and disable it in the Django admin.
3. Use an API endpoint that requires authentication and access control.
4. Make a request with the disabled user’s credentials.
5. The response incorrectly allows access to the protected resource, even though the user is disabled.

### **Expected behavior**
When a user’s account is disabled, they should not be able to access any protected resources, and the request should return a proper "403 Forbidden" or similar error.

### **Screenshots**
(If applicable, add screenshots that demonstrate the issue.)

### **Desktop (please complete the following information):**
 - OS: [e.g. Windows 10]
 - Browser: [e.g. Chrome]
 - Version: [affected version]

### **Smartphone (please complete the following information):**
 - Device: [e.g. iPhone 12]
 - OS: [e.g. iOS 14.4]
 - Browser: [e.g. Safari]
 - Version: [affected version]

### **Additional context**
This issue was identified in `djangorestframework-simplejwt` version 5.3.1 and earlier, where missing user validation checks in the `for_user` method cause the disabled users to still access resources. This may lead to security vulnerabilities such as unauthorized data access.
