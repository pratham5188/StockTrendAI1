# 🔧 Streamlit Cloud Deployment Troubleshooting

## 🚨 **Dependency Processing Error Solutions**

### **Problem**: "Error during processing dependencies"

### **Solution 1: Use Minimal Requirements**
If you encounter dependency conflicts, use the minimal requirements file:

1. **Rename files**:
   - Rename `requirements.txt` to `requirements_backup.txt`
   - Rename `requirements_minimal.txt` to `requirements.txt`

2. **Deploy again** with the minimal requirements

### **Solution 2: Remove Problematic Dependencies**
Some packages may cause conflicts. Try removing these from requirements.txt:
- `statsmodels` (can be problematic)
- `altair` (if not essential)
- `pydeck` (if not essential)

### **Solution 3: Use Compatible Versions**
The current `requirements.txt` uses version ranges instead of exact versions to avoid conflicts.

### **Solution 4: Check Python Version**
Ensure your Streamlit Cloud deployment uses Python 3.9 or higher.

## 🔍 **Common Issues and Fixes**

### **Issue 1: Prophet Installation Fails**
**Fix**: Prophet requires specific system dependencies. The `packages.txt` file includes these.

### **Issue 2: XGBoost/LightGBM Conflicts**
**Fix**: These are now using version ranges to allow compatible versions.

### **Issue 3: NumPy/Pandas Version Conflicts**
**Fix**: Using compatible version ranges instead of exact versions.

### **Issue 4: Streamlit Version Issues**
**Fix**: Using `streamlit>=1.47.0,<2.0.0` for compatibility.

## 📋 **Deployment Checklist**

### **Before Deployment:**
1. ✅ Use `requirements.txt` with version ranges
2. ✅ Ensure `packages.txt` is present
3. ✅ Verify `.streamlit/config.toml` is correct
4. ✅ Check that `app.py` is the main file

### **During Deployment:**
1. ✅ Monitor build logs for specific errors
2. ✅ If errors occur, try the minimal requirements
3. ✅ Check Python version compatibility

### **After Deployment:**
1. ✅ Test all app features
2. ✅ Verify data loading works
3. ✅ Check all tabs function properly

## 🛠️ **Quick Fixes**

### **If Build Fails:**
1. **Try minimal requirements**: Use `requirements_minimal.txt`
2. **Remove optional packages**: Comment out non-essential dependencies
3. **Check logs**: Look for specific package conflicts

### **If App Starts But Has Issues:**
1. **Check import errors**: Look for missing modules
2. **Verify data access**: Test YFinance connectivity
3. **Test ML models**: Ensure fallbacks work

## 📞 **Emergency Solutions**

### **Last Resort - Ultra Minimal Requirements:**
```txt
streamlit
pandas
numpy
plotly
yfinance
scikit-learn
```

### **Alternative - Use Only Core Dependencies:**
```txt
streamlit>=1.47.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
yfinance>=0.2.18
```

## 🎯 **Success Indicators**

### **✅ Deployment Successful When:**
- Build completes without errors
- App starts and shows the main interface
- All tabs are accessible
- Data loading works
- Charts render properly

### **❌ Deployment Failed When:**
- Build process fails
- App doesn't start
- Import errors in logs
- Missing dependencies

## 🚀 **Recommended Approach**

1. **Start with current `requirements.txt`** (version ranges)
2. **If that fails, use `requirements_minimal.txt`**
3. **If still failing, use ultra minimal requirements**
4. **Monitor logs for specific error messages**

**Status: 🔧 READY FOR TROUBLESHOOTING**