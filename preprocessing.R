library(rjson)
library(tidyverse)


read_results <- function(file_path)
{
  con <- file(file_path, open = "r")
  on.exit(close(con))
  lines <- readLines(con)
  
  subjects_data <- list()
  
  subj <- 0
  for (line in lines) {
    if (grepl("pre_questionnaire_3_prolific_id", line, fixed = TRUE))
    {
      subj = subj + 1
      metadata_beginning <-
        fromJSON(str_replace(line, "\\}\\{", ","))
      subj_data <- ""
    }
    else if ((grepl("{", line, fixed = TRUE) &
              grepl("post_questionnaire_1", line, fixed = TRUE)))
    {
      metadata_end <- fromJSON(line)
      
      df <-
        read.table(
          text = subj_data,
          sep = ",",
          header = TRUE,
          stringsAsFactors = FALSE
        )
      
      for (val in names(metadata_beginning))
      {
        df[paste(val, "_begin_quest")] <- metadata_beginning[val]
      }
      
      for (val in names(metadata_end))
      {
        df[paste(val, "_end_quest")] <- metadata_end[val]
      }
      
      subjects_data[[subj]] <- df
    }
    else if (!grepl("{", line, fixed = TRUE))
    {
      subj_data = paste(subj_data, line, "\n")
    }
  }
  return(subjects_data)
}