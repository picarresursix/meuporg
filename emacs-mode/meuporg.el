
(setq meuporg-command "python ~/.meuporg ")

(defun meuporg-reload()
  "Reload the current meuporg."
  (interactive)
  (save-buffer)
  (shell-command (concat meuporg-command " -u"))
  )

(defun meuporg-find-main()
  "Returns the path to meuporg of which the current file depends or an
empty string if there is no such meuporg."
  (setq old-buffer (current-buffer))
  (shell-command (concat meuporg-command " -f"))
  (switch-to-buffer "*Shell Command Output*")
  (setq path-to-main-meuporg
        (buffer-substring-no-properties (point-min) (- (point-max) 1))
        )
  (switch-to-buffer old-buffer)
  path-to-main-meuporg
  )

(defun meuporg-open-main()
  "Open the meuporg of which the current file depends (if any)."
  (interactive)
  (setq path-to-main-meuporg (meuporg-find-main))
  (if (< 2 (length path-to-main-meuporg))
      (progn
        (find-file path-to-main-meuporg)
        (message (concat "Opening " path-to-main-meuporg))
        )
      (message "No meuporg found.")
      )
  )

(defun meuporg-insert-todo()
  "Inserts a TODO meuporg item."
  (interactive)
  (insert "!TODO! ")
  )

(defun meuporg-insert-idea()
  "Inserts an IDEA meuporg item."
  (interactive)
  (insert "!IDEA! ")
  )

(defun meuporg-insert-tocheck()
  "Inserts a TOCHECK meuporg item."
  (interactive)
  (insert "!TOCHECK! ")
  )

(defun meuporg-insert-fixref()
  "Inserts a FIXREF meuporg item."
  (interactive)
  (insert "!FIXREF! ")
  )

(defun meuporg-go-to-next-item()
  (interactive)
  (condition-case ex
      (search-forward-regexp "\![a-zA-Z0-9_]*\!")
    ('error
     (message "No items after cursor.")
     )
    )
  )

(defun meuporg-go-to-previous-item()
  (interactive)
  (condition-case ex
      (search-backward-regexp "\![a-zA-Z0-9_]*\!")
    ('error
     (message "No items before cursor.")
     )
    )
  )

(global-unset-key (kbd "C-!"))

(define-minor-mode meuporg-mode
    "Toggle meuporg mode.

  Interactively with no argument, this command toggles the mode.
  A positive prefix argument enables the mode, any other prefix
  argument disables it.  From Lisp, argument omitted or nil enables
  the mode, `toggle' toggles the state. "
   ;; The initial value.
   :init-value nil
   ;; The indicator for the mode line.
   :lighter " !M!"
   :keymap
   `(
     (,(kbd "C-! u")   . meuporg-reload)
     (,(kbd "C-! m")   . meuporg-open-main)
     (,(kbd "C-! n")   . meuporg-go-to-next-item)
     (,(kbd "C-! p")   . meuporg-go-to-previous-item)
     (,(kbd "C-! i t") . meuporg-insert-todo)
     (,(kbd "C-! i i") . meuporg-insert-idea)
     (,(kbd "C-! i c") . meuporg-insert-tocheck)
     (,(kbd "C-! i f") . meuporg-insert-fixref)
     )
   )

(add-hook 'meuporg-mode-hook
         (lambda ()
           (font-lock-add-keywords nil '(("!\\([a-zA-Z0-9_]*\\)!" 1 font-lock-warning-face t)))
           )
         )

(add-hook 'find-file-hook
          (lambda()
            (if (< 1 (length (meuporg-find-main)))
                (meuporg-mode)
              )
            )
          )