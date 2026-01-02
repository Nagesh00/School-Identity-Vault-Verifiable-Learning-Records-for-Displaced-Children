# Contributing to School Identity Vault

We welcome contributions from developers, designers, and education specialists. Please follow these guidelines.

## Code of Conduct

- Be respectful and inclusive
- Focus on the mission: helping displaced children
- Respect user privacy and data security
- Collaborate openly

## Development Workflow

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/School-Identity-Vault...git
cd School-Identity-Vault...
```

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes
- Follow project code style
- Add tests for new functionality
- Update documentation

### 4. Commit with Clear Messages
```bash
git commit -m "feat: add document verification"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Code style
- refactor: Code refactoring
- test: Tests
- chore: Build/dependencies

**Example:**
```
feat(document-upload): add multi-language OCR support

Added support for Arabic, French, and Amharic OCR
using Azure Computer Vision multilingual API.

Fixes #123
```

## Testing

```bash
# Backend tests
cd backend
npm test

# Frontend tests
cd frontend
npm test

# ML Engine tests
cd ml-engine
pytest
```

## Code Style

### JavaScript/TypeScript
- Use ESLint configuration
- 2-space indentation
- Semicolons required

### Python
- Follow PEP 8
- Use Black formatter
- 4-space indentation

### Solidity
- Follow Solidity style guide
- Use 4-space indentation
- Add natspec comments

## Documentation

- Document new features
- Update API documentation
- Add architectural diagrams if needed
- Include usage examples

## Reporting Issues

### Bug Report Template
```markdown
**Describe the bug:**
[Clear description]

**Steps to reproduce:**
1. Step 1
2. Step 2

**Expected behavior:**
[What should happen]

**Actual behavior:**
[What actually happens]

**Screenshots/Logs:**
[If applicable]

**Environment:**
- OS: 
- Node version:
- Python version:
```

### Feature Request Template
```markdown
**Is your feature related to a problem?**
[Description]

**Describe the solution:**
[Clear description]

**Describe alternatives:**
[Other approaches considered]

**Impact:**
[How this benefits displaced children]
```

## Review Process

1. **Code Review**: At least one maintainer reviews
2. **Tests**: All tests must pass
3. **CI/CD**: Automated checks pass
4. **Documentation**: Changes documented
5. **Approval**: Maintainer approves
6. **Merge**: Feature branch merged to main

## Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] Tests pass locally
- [ ] No breaking changes without discussion

## Contact

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Email: team@schoolidentityvault.org

Thank you for contributing!
