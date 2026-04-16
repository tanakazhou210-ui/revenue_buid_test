# Revenue Forecast Tester AI Agent

## Project Overview
- **Project Name**: Revenue Forecast Tester
- **Type**: Streamlit Web Application
- **Core Functionality**: AI-powered tool to test and validate revenue forecasts with data upload, analysis, and visualization
- **Target Users**: Revenue analysts, data scientists, business planners

## UI/UX Specification

### Layout Structure
- **Header**: App title with icon, subtitle
- **Sidebar**: Navigation tabs for different features
- **Main Area**: Dynamic content based on selected feature
- **Footer**: None

### Visual Design
- **Color Palette**:
  - Background: `#0E1117` (dark theme)
  - Card Background: `#1E293B`
  - Primary Accent: `#10B981` (emerald green)
  - Secondary Accent: `#F59E0B` (amber)
  - Text Primary: `#F8FAFC`
  - Text Secondary: `#94A3B8`
  - Chart Colors: `#10B981`, `#3B82F6`, `#F59E0B`, `#EF4444`, `#8B5CF6`
- **Typography**:
  - Headings: Sans-serif, bold
  - Body: Sans-serif, regular
  - Font sizes: H1=32px, H2=24px, Body=16px
- **Spacing**: 16px base unit, 24px section gaps
- **Visual Effects**: Subtle shadows on cards, smooth transitions

### Components
1. **Data Upload Section**: File uploader (CSV/Excel), data preview table
2. **AI Chat Interface**: Chat input, message display, loading states
3. **Chart Builder**: Interactive chart controls, chart display area
4. **Analysis Dashboard**: KPI cards, summary stats, charts

## Functionality Specification

### Core Features

1. **Data Upload**
   - Accept CSV and Excel files
   - Display data preview (first 10 rows)
   - Show data statistics (columns, rows, types)
   - Store data in session state

2. **AI Analysis Agent**
   - Chat interface for asking questions about revenue data
   - Uses local LLM or basic analysis (no external API needed for demo)
   - Provides insights, identifies patterns, validates forecasts

3. **Chart Bot**
   - Interactive chart builder
   - Choose chart type: Line, Bar, Area, Scatter
   - Select X and Y columns
   - Multiple chart support
   - Export charts as images

4. **Forecast Testing**
   - Compare actual vs predicted revenue
   - Calculate accuracy metrics (MAPE, RMSE, MAE)
   - Generate residual analysis
   - Flag anomalies/outliers

### User Interactions
- Upload file → Auto-detect columns → Show preview
- Ask questions → Get AI responses about data
- Configure charts → Real-time chart updates
- Run tests → Display accuracy metrics

## Acceptance Criteria
- [ ] File upload works for CSV/Excel
- [ ] Data preview displays correctly
- [ ] AI chat responds to revenue questions
- [ ] Charts render with selected columns
- [ ] Accuracy metrics calculate correctly
- [ ] App runs without errors in Streamlit
